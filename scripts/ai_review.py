import os
import sys
import requests
import json

# Переменные окружения
GH_TOKEN = os.environ.get("GH_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"

# Для Google Sheets
APPS_SCRIPT_URL = os.environ.get("APPS_SCRIPT_URL")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
STUDENT_NAME = os.environ.get("GITHUB_ACTOR", "unknown")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY", "unknown")

def review_code_with_llm(code_to_review):
    """Отправляет код в GitHub Models и возвращает рецензию."""
    if not GH_TOKEN:
        return "Ошибка: GH_TOKEN не задан. Пожалуйста, настройте Secret в репозитории."

    prompt = (
        "Ты — строгий преподаватель Python. Задание: реализовать функцию find_multiples_of_3(), "
        "которая возвращает список всех чисел от 1 до 1000, кратных 3. "
        "Оцени код по критериям:\n"
        "1. Правильность (должен возвращаться правильный список).\n"
        "2. Эффективность (использование list comprehensions или цикла без лишних операций).\n"
        "3. Читаемость (понятные имена переменных, комментарии, отсутствие магических чисел).\n"
        "Формат ответа: Оценка: X/5, плюсы, минусы, советы."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GH_TOKEN}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Ты — полезный ассистент-преподаватель."},
            {"role": "user", "content": prompt + f"\n\nКод студента:\n```python\n{code_to_review}\n```"}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при обращении к API: {e}"

def send_to_google_sheets(review_text):
    if not APPS_SCRIPT_URL:
        print("APPS_SCRIPT_URL не задан, пропускаем отправку в Google Sheets.")
        return

    # ... (парсинг оценки и комментария остается как у вас) ...

    # Формируем payload так, как его ждет Apps Script
    payload = {
        "student": STUDENT_NAME,
        "assignment": REPO_NAME,
        "grade": grade,
        "comment": review_text
    }

    # Правильные заголовки для JSON
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Отправка данных в Google Sheets: {payload}")
    try:
        # ВАЖНО: используем json=payload, чтобы requests сам установил Content-Type
        response = requests.post(APPS_SCRIPT_URL, json=payload, headers=headers)
        print(f"Результат отправки. Статус: {response.status_code}, Ответ: {response.text}")
        response.raise_for_status() # Это вызовет исключение при плохом статусе
    except Exception as e:
        print(f"Не удалось отправить результат в Google Sheets: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Укажите путь к файлу с кодом, например: python ai_review.py solution.py")
        sys.exit(1)

    code_file = sys.argv[1]
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            student_code = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {code_file} не найден.")
        sys.exit(1)

    print("Отправляю код на проверку ИИ...")
    review = review_code_with_llm(student_code)
    
    # Выводим отчёт в консоль (для логов)
    print("\n--- Отчёт ИИ-преподавателя ---")
    print(review)
    print("--------------------------------")
    
    # Отправляем в Google Sheets
    send_to_google_sheets(review)
