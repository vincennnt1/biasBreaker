chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.isNews && sender.tab && sender.tab.id !== undefined) {
    chrome.action.setPopup({
      tabId: sender.tab.id,
      popup: "popup.html"
    });

    chrome.storage.local.set({ latestNewsCheck: msg.data });
  }
});
