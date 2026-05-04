import os
import sys
import requests
import json

GITHUB_TOKEN = os.environ.get("GH_TOKEN")
# Новый API-адрес GitHub Models (актуальный на 2025 год)
MODEL_API_URL = "https://models.github.ai/inference/chat/completions"

def review_code_with_llm(code_to_review):
    if not GITHUB_TOKEN:
        print("Ошибка: GITHUB_TOKEN не задан!")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    prompt = f"""
    Ты — строгий преподаватель информатики.
    Проверь следующий код на Python. Задание: функция должна считать количество вхождений подстроки (регистронезависимо).
    Оцени работу по шкале 1-5, где 5 — отлично.
    Напиши оценку и краткий комментарий с указанием ошибок или плюсов.

    Код студента:
    ```python
    {code_to_review}