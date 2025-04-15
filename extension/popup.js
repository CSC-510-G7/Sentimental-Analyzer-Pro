const analyzeFullButton = document.getElementById("analyze-full");
const analyzeSelectedButton = document.getElementById("analyze-selected");
const analyzeSelectedText = document.getElementById("analyze-selected-text");
const loadingIndicator = document.getElementById("loading-indicator");
const resultsContainer = document.getElementById("results");
let loading = false;

chrome.storage.local.get({ loading: false, analysisResult: null }, (result) => {
  if (result.loading) {
    loading = true;
    analyzeFullButton.disabled = true;
    analyzeSelectedButton.disabled = true;
    analyzeSelectedText.hidden = true;
    resultsContainer.hidden = true;
    loadingIndicator.hidden = false;
  }
  else if (result.analysisResult) {
    renderAnalysisResult(result.analysisResult);
  }
});

// On popup load, check for active text selection in the current tab
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if (!tabs || tabs.length === 0) {
    console.error("No active tab found.");
    return;
  }
  
  const activeTab = tabs[0];

  // Inject a script to get the selected text
  chrome.scripting.executeScript(
    {
      target: { tabId: activeTab.id },
      func: () => window.getSelection().toString() // Get the selected text
    },
    (results) => {
      if (results && results[0] && results[0].result) {
        if (loading) return;
        const selectedText = results[0].result;

        if (selectedText) {
          // Enable the "Analyze Selected" button and set up its click handler
          analyzeSelectedButton.disabled = false;
          analyzeSelectedText.hidden = true;
          analyzeSelectedButton.addEventListener("click", () => {
            chrome.runtime.sendMessage({ type: "analyze", text: selectedText, openPopup: false, source: activeTab.url });
          });
        } else {
          // No text is selected
          analyzeSelectedButton.disabled = true;
          analyzeSelectedText.hidden = false;
        }
      }
    }
  );
});

// Listen for message from background script when analysis completes
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type.startsWith("analysis-")) {
    loadingIndicator.hidden = true;
    analyzeFullButton.disabled = false;
    analyzeSelectedButton.disabled = false;
    analyzeSelectedText.hidden = true;
  
    if (message.type === "analysis-result") {
      renderAnalysisResult(message.data);
    }
  } else if (message.type === "selection-update") {
    if (message.text) {
      analyzeSelectedButton.disabled = false;
      analyzeSelectedText.hidden = true;

      analyzeSelectedButton.disabled = false;
      analyzeSelectedText.hidden = true;
      analyzeSelectedButton.addEventListener("click", () => {
        chrome.runtime.sendMessage({ type: "analyze", text: message.text, openPopup: false, source: sender.url });
      });
    } else {
      analyzeSelectedButton.disabled = true;
      analyzeSelectedText.hidden = false;
    }
  }
});


// Handle full page analysis
analyzeFullButton.addEventListener("click", () => {
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs || tabs.length === 0) {
      console.error("No active tab found.");
      return;
    }

    const activeTab = tabs[0];

    // Inject a script to extract the page content
    chrome.scripting.executeScript(
      {
        target: { tabId: activeTab.id },
        func: () => document.body.innerText // Extract the page's text content
      },
      (results) => {
        if (results && results[0] && results[0].result) {
          const pageContent = results[0].result;

          console.log("Page content:", pageContent);

          chrome.storage.local.set({ loading: true }, () => {
            loading = true;
            analyzeFullButton.disabled = true;
            analyzeSelectedButton.disabled = true;
            analyzeSelectedText.hidden = true;
            loadingIndicator.hidden = false;
            resultsContainer.hidden = true;
          });

          // Send the extracted content to the background script for analysis
          chrome.runtime.sendMessage({ type: "analyze", text: pageContent, openPopup: false, source: activeTab.url });
        }
      }
    );
  });
});


function renderAnalysisResult(result) {
  resultsContainer.hidden = false;
  document.querySelector("#results-source a").innerText = result.source_url;
  document.querySelector("#results-source a").href = result.source_url;
  document.querySelector("#results-target").href = result.results_url;

  // Extract sentiment values
  const { pos, neu, neg } = result.sentiment;

  // Calculate percentages
  const posPercent = (pos * 100).toFixed(1);
  const neuPercent = (neu * 100).toFixed(1);
  const negPercent = (neg * 100).toFixed(1);

  // Update sentiment bar widths
  document.getElementById("sentiment-pos").style.width = `${posPercent}%`;
  document.getElementById("sentiment-neu").style.width = `${neuPercent}%`;
  document.getElementById("sentiment-neg").style.width = `${negPercent}%`;

  // Update sentiment percentages text
  document.getElementById("sentiment-percentages").innerHTML = 
    `<div style="display: flex; justify-content: space-between"><div>Pos: ${posPercent}%</div><div>Neu: ${neuPercent}%</div> <div>Neg: ${negPercent}%</div></div>`;
}
