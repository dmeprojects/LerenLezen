async function fetchState() {
  const response = await fetch("/api/state");
  const state = await response.json();
  render(state);
}

function render(state) {
  document.getElementById("current-word").textContent = state.current_word;
  document.getElementById("wpm").textContent = state.wpm;
  document.getElementById("words-left").textContent = state.words_left;
  document.getElementById("good-checks").textContent = state.good_checks;
  document.getElementById("bad-checks").textContent = state.bad_checks;
  document.getElementById("stars").textContent = state.stars;
  document.getElementById("sads").textContent = state.sads;
}

async function sendAnswer(correct) {
  const response = await fetch("/api/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correct })
  });
  const state = await response.json();
  render(state);
}

async function resetGame() {
  const response = await fetch("/api/reset", { method: "POST" });
  const state = await response.json();
  render(state);
}

document.getElementById("correct-btn").addEventListener("click", () => sendAnswer(true));
document.getElementById("wrong-btn").addEventListener("click", () => sendAnswer(false));
document.getElementById("reset-btn").addEventListener("click", resetGame);

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    sendAnswer(true);
  } else if (event.key === "ArrowLeft") {
    sendAnswer(false);
  }
});

fetchState();