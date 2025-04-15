chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "analyze") {
    queryTextAnalysis(message.text, message.source);
    chrome.storage.local.set({ loading: true }, () => {
      if (message.openPopup) {
        chrome.action.openPopup();
      }
    });
  }
});

function queryTextAnalysis(text, source) {
  console.log("Querying text analysis");

  fetch('http://localhost:8000/textanalysis', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: new URLSearchParams({
      'textField': text
    })
  })
    .then(response => response.json())
    .then(data => {
      data.source_url = source;
      console.log('Success:', data);
      chrome.storage.local.set({ loading: false, analysisResult: data }, () => {
        chrome.runtime.sendMessage({ type: "analysis-result", data: data });
      });
    })
    .catch(error => {
      console.error('Error:', error);
      chrome.storage.local.set({ loading: false }, () => {
        chrome.runtime.sendMessage({ type: "analysis-error", error: error });
      });
    }
  );
}
