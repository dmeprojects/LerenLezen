function renderIcons(containerId, count, imageSrc, altText) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  for (let i = 0; i < count; i++) {
    const img = document.createElement("img");
    img.src = imageSrc;
    img.alt = altText;
    img.className = "score-icon";
    container.appendChild(img);
  }
}

function render(state) {
  const currentWord = document.getElementById("current-word");
  const wpm = document.getElementById("wpm");
  const wordsLeft = document.getElementById("words-left");

  if (currentWord) currentWord.textContent = state.current_word;
  if (wpm) wpm.textContent = state.wpm;
  if (wordsLeft) wordsLeft.textContent = state.words_left;

  renderIcons("good-checks", state.good_checks, window.APP_ICONS.greenCheck, "good");
  renderIcons("bad-checks", state.bad_checks, window.APP_ICONS.redCheck, "bad");
  renderIcons("stars", state.stars, window.APP_ICONS.star, "star");
  renderIcons("sads", state.sads, window.APP_ICONS.sad, "sad");
}

async function fetchState() {
  const response = await fetch("/api/state");
  const state = await response.json();
  render(state);
}

async function sendAnswer(correct) {
  const response = await fetch("/api/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correct: correct })
  });
  const state = await response.json();
  render(state);
}

async function resetGame() {
  const response = await fetch("/api/reset", {
    method: "POST"
  });
  const state = await response.json();
  render(state);
}

document.addEventListener("DOMContentLoaded", function () {
  const correctBtn = document.getElementById("correct-btn");
  const wrongBtn = document.getElementById("wrong-btn");
  const resetBtn = document.getElementById("reset-btn");

  if (correctBtn) correctBtn.addEventListener("click", () => sendAnswer(true));
  if (wrongBtn) wrongBtn.addEventListener("click", () => sendAnswer(false));
  if (resetBtn) resetBtn.addEventListener("click", resetGame);

  document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowRight") {
      sendAnswer(true);
    } else if (event.key === "ArrowLeft") {
      sendAnswer(false);
    }
  });

  fetchState();
});