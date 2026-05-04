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
        "Ты — строгий, но справедливый преподаватель информатики.\n"
        "Проанализируй следующий код на Python. Задание: реализовать функцию count_substring_occurrences,\n"
        "которая подсчитывает количество вхождений подстроки в строку (без учёта регистра).\n"
        "Оцени код по следующим критериям: правильность, стиль, эффективность.\n"
        "Если код правильный, поставь оценку 5/5 и кратко похвали.\n"
        "Если есть ошибки или недочёты, укажи их и поставь оценку 2/5 или 3/5.\n"
        "Ответ должен быть в формате: Оценка: X/5. Затем пояснение.\n\n"
        "Вот код студента:\n"
        f"```python\n{code_to_review}\n```"
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
