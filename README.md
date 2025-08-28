# 🎮 QuizMaster – OOP-Based Terminal Quiz Game

QuizMaster is a Python-based interactive quiz system that runs in the terminal.  
It uses **Object-Oriented Programming (OOP)** principles and allows users to choose categories, answer multiple-choice questions, and get instant feedback with scoring.

---

## 🚀 Features
- Category-based question selection  
- Multiple Choice Questions (MCQs)  
- Score calculation & percentage display  
- Performance feedback (Excellent, Good, Try Again)  
- Loads quizzes from external JSON file (`questions.json`)  

---

## 🛠️ Project Structure
QuizMaster/
│
├── quizmaster.py # Main Python script (game logic)
├── questions.json # Question bank (editable)
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/quizmaster.git
cd quizmaster
2. Install Python
Make sure Python 3.8+ is installed on your system.

Check version:

bash
Copy code
python --version
3. Add Questions
Edit the questions.json file to add your own questions in this format:

json
Copy code
{
  "General Knowledge": [
    {
      "question_text": "What is the capital of France?",
      "options": ["Paris", "Berlin", "London", "Rome"],
      "correct_option": 0
    }
  ],
  "Math": [
    {
      "question_text": "What is 12 * 8?",
      "options": ["96", "108", "86", "112"],
      "correct_option": 0
    }
  ]
}
▶️ How to Run
Open a terminal in the project folder.

Run the game:

bash
Copy code
python quizmaster.py
Select a category and start answering questions!

📝 Feedback Messages
90%+ → Excellent! 🎉

70% – 89% → Good Job! 👍

50% – 69% → Keep Practicing 🙂

Below 50% → Try Again! 💪

👨‍💻 Author
Developed by [Your Name]

pgsql
Copy code

Do you want me to also make the README **GitHub-friendly with badges** (like Python version, repo stars, license), or keep it simple like this?
