document.getElementById("check").addEventListener("click", async () => {
  const resultEl = document.getElementById("result");
  resultEl.innerText = "Checking...";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  try {
    const res = await fetch(`http://localhost:5000/check-url?url="${encodeURIComponent(url)}"`);
    const data = await res.json();

    if (data.error) {
      resultEl.innerText = "Error: " + data.error;
    } else {
      resultEl.innerHTML = `
        <p><strong>Title:</strong> ${data.title}</p>
        <p><strong>Score:</strong> ${(data.weighted_score * 100).toFixed(1)}%</p>
        <p style="font-weight: bold; color: ${data.is_real === "true" ? '#2e7d32' : '#c62828'};">
          ${data.is_real === "true" ? "Credible Source" : "Possibly Fake News"}
        </p>
      `;
    }
  } catch (err) {
    resultEl.innerText = "Failed to connect to local server. Make sure Tru app is launched.";
  }
});
