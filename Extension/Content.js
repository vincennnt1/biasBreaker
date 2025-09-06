(async () => {
  const url = window.location.href;

  try {
    const res = await fetch(`http://localhost:5000/check-url?url=${encodeURIComponent(url)}`);

    const data = await res.json();

    if (!data.error && data.title_score && data.text_score) {
      chrome.runtime.sendMessage({ isNews: true, data });
    }
  } catch (err) {
    console.error("Error contacting local server:", err);
  }
})();
