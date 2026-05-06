import os
import sys
import requests
import json

# Переменная окружения GH_TOKEN должна быть передана из GitHub Secrets
GH_TOKEN = os.environ.get("GH_TOKEN")
# Актуальный эндпоинт GitHub Models на май 2026 года
API_URL = "https://models.github.ai/inference/chat/completions"

def review_cpp_code_with_llm(code_to_review):
    """
    Отправляет C++ код студента в GitHub Models (GPT-4o mini) и возвращает рецензию.
    """
    if not GH_TOKEN:
        return "Ошибка: GH_TOKEN не задан. Пожалуйста, настройте Secret в репозитории."

    # Промпт для ИИ, адаптированный под C++
    prompt = (
        "Ты — строгий, но справедливый преподаватель курса 'Программирование на C++'.\n"
        "Проанализируй следующий код на C++. Задание может быть любым (функция, класс, алгоритм).\n"
        "Оцени код по следующим критериям (каждый от 0 до 2 баллов):\n"
        "1. Корректность (правильно ли решена задача, обработка крайних случаев).\n"
        "2. Эффективность (оптимальность алгоритма, использование ресурсов).\n"
        "3. Стиль и читаемость (имена переменных, отступы, комментарии, отсутствие магических чисел).\n"
        "4. Безопасность и управление памятью (отсутствие утечек, корректная работа с указателями/ссылками).\n"
        "Итоговая оценка — среднее арифметическое, округлённое до целого, по 5-балльной шкале.\n"
        "Формат ответа:\n"
        "Оценка: X/5\n"
        "Плюсы: ...\n"
        "Минусы: ...\n"
        "Советы по улучшению: ...\n\n"
        "Вот код студента:\n"
        f"```cpp\n{code_to_review}\n```"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GH_TOKEN}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Ты — опытный преподаватель C++."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1200
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
        print("Укажите путь к файлу с C++ кодом, например: python ai_review_cpp.py solution.cpp")
        sys.exit(1)

    code_file = sys.argv[1]
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            student_code = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {code_file} не найден.")
        sys.exit(1)

    print("Отправляю C++ код на проверку ИИ...")
    review = review_cpp_code_with_llm(student_code)
    print("\n--- Отчёт ИИ-преподавателя (C++) ---")
    print(review)
    print("--------------------------------------")
