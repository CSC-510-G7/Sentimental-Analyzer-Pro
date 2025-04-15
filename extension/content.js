function createAnalyzeSelectedButton(selection) {
  const btn = document.createElement("button");
  btn.id = "analyze-selected-btn";
  btn.textContent = "Analyze Selected Text";
  btn.addEventListener("click", () => {
    const text = window.getSelection().toString();
    if (text) {
      chrome.runtime.sendMessage({ type: "analyze", text, openPopup: true, source: window.location.href });
    }
  });

  // Get the position of the selection
  const rect = selection.getRangeAt(0).getBoundingClientRect();
  console.log(selection.getRangeAt(0));

  // Position the button at the bottom-right corner of the selection
  btn.style.left = `${rect.left + window.scrollX}px`; // 10px offset from the right edge
  btn.style.top = `${rect.top + window.scrollY - 40}px`; // 10px offset from the top edge
  btn.style.zIndex = "9999"; // Ensure it's on top of other elements
  document.body.appendChild(btn);
}

function removeAnalyzeSelectedButton() {
  const btn = document.getElementById("analyze-selected-btn");
  if (btn) {
    btn.remove();
  }
}

let lastSelection = "";

// Send selection updates to the background script
function updateSelectionInBackground(selectedText) {
  chrome.runtime.sendMessage({
    type: "selection-update",
    text: selectedText || null, // Send null if no selection
  });
}

// Listen for the mouseup event to show the button and send selection updates
document.addEventListener("mouseup", () => {
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const selectedText = selection.toString();
    if (selectedText && selectedText !== lastSelection) {
      lastSelection = selectedText;
      removeAnalyzeSelectedButton();
      createAnalyzeSelectedButton(selection);
      updateSelectionInBackground(selectedText); // Send the selected text
    }
  }
});

// Listen for the selectionchange event to remove the button and clear selection updates
document.addEventListener("selectionchange", () => {
  const selection = window.getSelection();
  if (!selection.toString()) {
    removeAnalyzeSelectedButton();
    updateSelectionInBackground(null); // Clear the selection
  }
});
