from flask import Flask, jsonify, render_template, request
from pathlib import Path
import random
import time

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
WORD_FILE = BASE_DIR  / "words" / "woorden_8a.txt"


def load_words(filename: Path) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().split()


class ReadingGame:
    def __init__(self, word_file: Path):
        self.word_file = word_file
        self.reset()

    def reset(self):
        self.words = load_words(self.word_file)
        random.shuffle(self.words)

        self.good_checks = 0
        self.bad_checks = 0
        self.stars = 0
        self.sads = 0
        self.wpm = 0
        self.last_time = time.time()

        self.current_word = self.words.pop(0) if self.words else "Geen woorden"
        self.words_left = len(self.words)

    def next_word(self):
        if not self.words:
            self.current_word = "Je bent klaar"
            self.words_left = 0
            return

        self.current_word = self.words.pop(0)
        self.words_left = len(self.words)

    def answer(self, correct: bool):
        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now

        if elapsed > 0:
            self.wpm = round(60 / elapsed)

        if correct:
            self.good_checks += 1
            if self.good_checks >= 10:
                self.stars += 1
                self.good_checks = 0
        else:
            self.bad_checks += 1
            if self.bad_checks >= 10:
                self.sads += 1
                self.bad_checks = 0
                self.good_checks = 0

        self.next_word()

    def state(self):
        return {
            "current_word": self.current_word,
            "words_left": self.words_left,
            "wpm": self.wpm,
            "good_checks": self.good_checks,
            "bad_checks": self.bad_checks,
            "stars": self.stars,
            "sads": self.sads,
        }


game = ReadingGame(WORD_FILE)


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/state")
def get_state():
    return jsonify(game.state())


@app.post("/api/answer")
def post_answer():
    data = request.get_json(silent=True) or {}
    correct = bool(data.get("correct", False))
    game.answer(correct)
    return jsonify(game.state())


@app.post("/api/reset")
def reset():
    game.reset()
    return jsonify(game.state())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)