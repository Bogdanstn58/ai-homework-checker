# tests/test_student_code.py
from solution import count_substring_occurrences

def test_simple_occurrence():
    """Проверяем обычный случай."""
    text = "Hello world, hello everyone!"
    substring = "hello"
    # Ожидаем 2, так как функция должна игнорировать регистр
    assert count_substring_occurrences(text, substring) == 2

def test_no_occurrence():
    """Подстрока не найдена."""
    text = "Happy coding!"
    substring = "python"
    assert count_substring_occurrences(text, substring) == 0

def test_empty_string():
    """Пустая строка."""
    text = ""
    substring = "word"
    assert count_substring_occurrences(text, substring) == 0