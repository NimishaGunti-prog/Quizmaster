"""
QuizMaster – OOP Terminal Quiz Game (timed, randomized, CSV export, simple GUI)
Save this file as quizmaster.py in the same folder as questions.json
"""

import json
import os
import sys
import textwrap
import random
import csv
import time
import threading
from typing import List, Dict

# optional GUI
try:
    import tkinter as tk
    from tkinter import messagebox
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False


class Question:
    def __init__(self, question_text: str, options: List[str], correct_option: int):
        self.question_text = question_text
        self.options = options
        self.correct_option = correct_option

    def is_correct(self, choice_index: int) -> bool:
        return choice_index == self.correct_option


class Quiz:
    def __init__(self, category: str, questions: List[Question], time_limit: int = 15):
        self.category = category
        self.questions = questions
        self.score = 0
        self.answered = 0
        self.time_limit = time_limit

    def start_quiz(self):
        print(f"\nStarting quiz: {self.category}\n")
        self.score = 0
        self.answered = 0

        # Randomize question order
        random.shuffle(self.questions)

        for idx, q in enumerate(self.questions, start=1):
            print(f"Question {idx}/{len(self.questions)}:")
            print(textwrap.fill(q.question_text, width=80))

            # Randomize options and keep mapping to original correct index
            option_map = list(enumerate(q.options))
            random.shuffle(option_map)
            shuffled_options = [opt for _, opt in option_map]
            correct_new_index = [i for i, (old_idx, _) in enumerate(option_map) if old_idx == q.correct_option][0]

            for opt_i, opt in enumerate(shuffled_options):
                label = chr(ord("A") + opt_i)
                print(f"  {label}. {opt}")

            user_choice = self._timed_input(len(shuffled_options), self.time_limit)
            if user_choice is None:
                print("Time up! No answer recorded.\n")
            elif user_choice == correct_new_index:
                print("Correct!\n")
                self.score += 1
            else:
                correct_label = chr(ord("A") + correct_new_index)
                print(f"Wrong. Correct answer: {correct_label}. {shuffled_options[correct_new_index]}\n")
            self.answered += 1

        self.show_result()

    def _timed_input(self, num_options: int, timeout: int):
        result = [None]

        def get_input():
            try:
                choice = input(f"Your answer (A-{chr(ord('A')+num_options-1)}) within {timeout}s: ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                return
            if not choice:
                return
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < num_options:
                    result[0] = idx
                    return
            if 'A' <= choice <= chr(ord('A')+num_options-1):
                result[0] = ord(choice) - ord('A')

        t = threading.Thread(target=get_input)
        t.daemon = True
        t.start()
        t.join(timeout)
        return result[0]

    def show_result(self):
        total = len(self.questions)
        pct = (self.score / total) * 100 if total else 0
        print("=" * 40)
        print(f"Quiz complete: {self.category}")
        print(f"Score: {self.score}/{total}")
        print(f"Percentage: {pct:.2f}%")
        feedback = self._feedback_for_pct(pct)
        print(f"Feedback: {feedback}")
        print("=" * 40)
        self._export_result(pct)

    def _export_result(self, pct):
        filename = "results.csv"
        file_exists = os.path.exists(filename)
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Category", "Score", "Total", "Percentage"])
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), self.category, self.score, len(self.questions), f"{pct:.2f}%"])

    @staticmethod
    def _feedback_for_pct(pct: float) -> str:
        if pct >= 90:
            return "Excellent — outstanding performance!"
        if pct >= 75:
            return "Very Good — keep it up!"
        if pct >= 50:
            return "Good — room for improvement."
        return "Try Again — practice more and try once more."


class QuizManager:
    def __init__(self, data_file: str = "questions.json"):
        self.data_file = data_file
        self.categories: Dict[str, List[Question]] = {}
        self._load_all_categories()

    def _load_all_categories(self):
        if not os.path.exists(self.data_file):
            print(f"Questions file '{self.data_file}' not found in current folder.")
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return

        # Expecting top-level key "categories": { "Category Name": [ {question_text,...}, ... ] }
        cats = raw.get("categories") or {}
        for cat_name, qlist in cats.items():
            parsed_questions = []
            for q in qlist:
                try:
                    parsed_questions.append(
                        Question(
                            question_text=q["question_text"],
                            options=q["options"],
                            correct_option=int(q["correct_option"]),
                        )
                    )
                except Exception as e:
                    print(f"Skipping invalid question in '{cat_name}': {e}")
            if parsed_questions:
                self.categories[cat_name] = parsed_questions

    def list_categories(self) -> List[str]:
        return list(self.categories.keys())

    def choose_category(self) -> str:
        cats = self.list_categories()
        if not cats:
            print("No categories available. Please populate 'questions.json' and restart.")
            sys.exit(1)

        print("Available categories:")
        for i, c in enumerate(cats, start=1):
            print(f"  {i}. {c} ({len(self.categories[c])} questions)")

        while True:
            try:
                raw = input(f"Choose a category (1-{len(cats)}): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                sys.exit(0)

            if raw.isdigit():
                n = int(raw)
                if 1 <= n <= len(cats):
                    return cats[n - 1]
            if raw in self.categories:
                return raw
            print("Invalid selection. Try again.")

    def start(self):
        print("\nWelcome to QuizMaster — OOP Terminal Quiz Game!\n")
        while True:
            category = self.choose_category()
            quiz = Quiz(category, self.categories[category])
            quiz.start_quiz()

            again = input("Would you like to try another category? (y/n/gui): ").strip().lower()
            if again == "gui":
                if TK_AVAILABLE:
                    self.start_gui()
                else:
                    print("Tkinter GUI not available on this Python interpreter.")
            if again not in ("y", "yes", "gui"):
                print("Thanks for playing QuizMaster. Goodbye!")
                break

    def start_gui(self):
        if not TK_AVAILABLE:
            print("Tkinter not available; cannot start GUI.")
            return

        root = tk.Tk()
        root.title("QuizMaster GUI")

        def run_category(cat):
            qlist = list(self.categories[cat])[:]
            random.shuffle(qlist)
            score = 0
            total = len(qlist)
            idx = 0

            lbl = tk.Label(root, text="", wraplength=400, justify="left")
            lbl.pack(pady=20)
            buttons = [tk.Button(root, text="", width=40) for _ in range(4)]
            for b in buttons:
                b.pack(pady=5)

            def show_question():
                nonlocal idx, score
                if idx >= total:
                    messagebox.showinfo("Result", f"Score: {score}/{total}")
                    root.destroy()
                    return
                q = qlist[idx]
                opts = list(enumerate(q.options))
                random.shuffle(opts)
                lbl.config(text=q.question_text)
                for b, (i, opt) in zip(buttons, opts):
                    b.config(text=opt, command=lambda i=i: check_answer(i))

            def check_answer(choice):
                nonlocal idx, score
                if qlist[idx].is_correct(choice):
                    score += 1
                idx += 1
                show_question()

            show_question()

        cat = self.choose_category()
        run_category(cat)
        root.mainloop()


def main():
    manager = QuizManager()
    manager.start()


if __name__ == "__main__":
    main()
