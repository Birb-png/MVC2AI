import requests
import json
import random
import time

# Question from Open Trivia Database
QUESTION_CATEGORIES = {
    "วิทยาศาสตร์": 17,   # Science & Nature
    "ความรู้ทั่วไป": 9,    # General
    "คำถามเชิงอารมณ์": 25  # Art (Represent Emotional :D)
}

# generate a 5-digit question ID 
# first digit not zero
def generate_question_id():
    return str(random.randint(1, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(4))

# fetching question from Open Trivia Database API
def get_questions_from_api(amount, category_id):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category_id}&type=multiple"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException:
        return []

# Format questions into the required JSON structure
def format_questions(raw_questions, category_name):
    formatted = []
    for q in raw_questions:
        formatted.append({
            "id": generate_question_id(),
            "type": category_name,
            "text": q["question"],
            "answer": q["correct_answer"]
        })
    return formatted

# Main
def main():
    print("Loading...")
    all_questions = {"questions": []}

    for category_name, category_id in QUESTION_CATEGORIES.items():
        attempts = 0
        while attempts < 3:  # try 3 times if API returns nothing
            raw_questions = get_questions_from_api(amount=20, category_id=category_id)
            if raw_questions:
                formatted_questions = format_questions(raw_questions, category_name)
                all_questions["questions"].extend(formatted_questions)
                break  # Exit loop if finish
            attempts += 1
            time.sleep(2)  # prevent limit somehow this worked

    # Ensure all categories have 10 questions
    for category_name in QUESTION_CATEGORIES.keys():
        count = sum(1 for q in all_questions["questions"] if q["type"] == category_name)
        if count < 10:
            print(f"Warning: Only {count} {category_name} questions found!")

    # Save to JSON file
    with open("questions.json", "w", encoding="utf-8") as f:
        print("finish")
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

# Run the script
if __name__ == "__main__":
    main()
