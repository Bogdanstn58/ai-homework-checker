import os
import sys
import requests
import json

# ... (предыдущий код функции review_code_with_llm и main без изменений) ...

if __name__ == "__main__":
    # ... (код для получения student_code и review) ...

    # 1. Получаем аргументы из CI/CD окружения
    student_name = os.environ.get("GITHUB_ACTOR", "unknown")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "unknown")
    
    # 2. Парсим оценку и комментарий из ответа ИИ
    #    Это зависит от формата, который вы задали в промпте.
    #    Для простоты предположим, что ответ имеет вид "Оценка: X/5. Комментарий..."
    grade = "N/A"
    comment = review
    if "Оценка:" in review:
        try:
            grade_part = review.split("Оценка:")[1].split(",")[0].strip()
            grade = grade_part
        except:
            pass

    # 3. Формируем данные для отправки
    payload = {
        "student": student_name,
        "assignment": repo_name,
        "grade": grade,
        "comment": comment
    }

    # 4. Отправляем POST-запрос к нашему Google Apps Script
    apps_script_url = os.environ.get("APPS_SCRIPT_URL")
    if apps_script_url:
        try:
            response = requests.post(apps_script_url, json=payload)
            print(f"Результат отправлен в Google Sheets. Статус: {response.status_code}")
        except Exception as e:
            print(f"Не удалось отправить результат в Google Sheets: {e}")
    else:
        print("APPS_SCRIPT_URL не задан, пропускаем отправку в Google Sheets.")

    # 5. Выводим отчёт в консоль (для отладки, студент его всё ещё может увидеть)
    print("\n--- Отчёт ИИ-преподавателя ---")
    print(review)
    print("--------------------------------")
