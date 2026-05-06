import os
import sys
import requests
import json

# Переменная окружения GH_TOKEN должна быть передана из GitHub Secrets
GH_TOKEN = os.environ.get("GH_TOKEN")
# Актуальный эндпоинт GitHub Models на май 2026 года
API_URL = "https://models.github.ai/inference/chat/completions"

def review_code_with_llm(code_to_review):
    """
    Отправляет код студента в GitHub Models (GPT-4o mini) и возвращает рецензию.
    """
    if not GH_TOKEN:
        return "Ошибка: GH_TOKEN не задан. Пожалуйста, настройте Secret в репозитории."

    # Промпт для ИИ (используем одинарные кавычки, чтобы избежать проблем со спецсимволами)
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
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        ai_reply = result['choices'][0]['message']['content']
        return ai_reply
    except requests.exceptions.RequestException as e:
        return f"Ошибка при обращении к API GitHub Models: {e}\nОтвет сервера: {response.text if 'response' in locals() else 'нет ответа'}"

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
    print("\n--- Отчёт ИИ-преподавателя ---")
    print(review)
    print("--------------------------------")
