import os
import sys
import requests
import json

GH_TOKEN = os.environ.get("GH_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"
APPS_SCRIPT_URL = os.environ.get("APPS_SCRIPT_URL")

def get_ai_review(code):
    if not GH_TOKEN:
        return "Ошибка: нет GH_TOKEN"
    
    prompt = f"Оцени код на Python:\n{code}\nДай оценку от 1 до 5 кратко."
    
    try:
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {GH_TOKEN}", "Content-Type": "application/json"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
        )
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка ИИ: {e}"

def send_to_sheets(grade, comment):
    if not APPS_SCRIPT_URL:
        print("Нет APPS_SCRIPT_URL")
        return
    try:
        payload = {
            "student": os.environ.get("GITHUB_ACTOR", "unknown"),
            "assignment": os.environ.get("GITHUB_REPOSITORY", "unknown"),
            "grade": grade,
            "comment": comment
        }
        resp = requests.post(APPS_SCRIPT_URL, json=payload)
        print(f"Google Sheets ответ: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Ошибка отправки в Sheets: {e}")

if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "solution.py"
    with open(file, "r") as f:
        code = f.read()
    
    review = get_ai_review(code)
    print("--- Отчёт ИИ ---")
    print(review)
    print("----------------")
    
    # Отправляем в Google Sheets
    send_to_sheets("N/A", review)  # grade можно распарсить из review
