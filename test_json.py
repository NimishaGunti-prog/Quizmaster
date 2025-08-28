import json
import sys

fname = "questions.json"
try:
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("✅ Loaded JSON file.")
    print("Top-level keys:", list(data.keys()))
    cats = data.get("categories") or {}
    print("Categories found:", list(cats.keys()))
    for cat, qs in cats.items():
        if not qs:
            print(f"  {cat}: no questions.")
            continue
        q0 = qs[0]
        print(f"\nSample from {cat}:")
        print(" question_text:", q0.get("question_text"))
        print(" options:", q0.get("options"))
        print(" correct_option (index):", q0.get("correct_option"))
except FileNotFoundError:
    print("❌ File not found:", fname)
    sys.exit(1)
except json.JSONDecodeError as e:
    print("❌ JSON decode error:", e)
    sys.exit(1)
