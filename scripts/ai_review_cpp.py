import os
import sys
import requests
import json

GH_TOKEN = os.environ.get("GH_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"
APPS_SCRIPT_URL = os.environ.get("APPS_SCRIPT_URL")

def get_ai_review_cpp(code):
    if not GH_TOKEN:
        return "Ошибка: нет GH_TOKEN"
    
    prompt = f"Ты строгий преподаватель C++. Оцени код по критериям: правильность, эффективность, стиль. Задание: найти максимальное число от 1 до 1000, кратное 9. Код:\n\n{code}\n\nОтвет в формате: Оценка: X/5. Плюсы, минусы, советы."
    
    try:
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {GH_TOKEN}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000
            }
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка ИИ: {e}"

def send_to_google_sheets(review_text):
    if not APPS_SCRIPT_URL:
        print("Нет APPS_SCRIPT_URL, пропускаем отправку в Google Sheets.")
        return
    
    # Парсим оценку (простой вариант)
    grade = "N/A"
    if "Оценка:" in review_text:
        try:
            grade_part = review_text.split("Оценка:")[1].split(",")[0].strip()
            grade = grade_part
        except:
            pass
    
    payload = {
        "student": os.environ.get("GITHUB_ACTOR", "unknown"),
        "assignment": os.environ.get("GITHUB_REPOSITORY", "unknown"),
        "language": "C++",
        "grade": grade,
        "comment": review_text
    }
    
    try:
        response = requests.post(APPS_SCRIPT_URL, json=payload)
        print(f"Google Sheets ответ (C++): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ошибка отправки в Sheets (C++): {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Укажите путь к файлу с C++ кодом, например: python ai_review_cpp.py solution.cpp")
        sys.exit(1)
    
    code_file = sys.argv[1]
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {code_file} не найден.")
        sys.exit(1)
    
    print("Отправляю C++ код на проверку ИИ...")
    review = get_ai_review_cpp(code)
    
    print("\n--- Отчёт ИИ-преподавателя (C++) ---")
    print(review)
    print("--------------------------------------")
    
    # Отправляем в Google Sheets
    send_to_google_sheets(review)
