from solution import find_multiples_of_3

def test_length():
    result = find_multiples_of_3()
    # Чисел, кратных 3, от 1 до 1000: floor(1000/3) = 333
    assert len(result) == 333, f"Ожидалось 333 числа, получено {len(result)}"

def test_all_multiples_of_3():
    result = find_multiples_of_3()
    for num in result:
        assert num % 3 == 0, f"Число {num} не кратно 3"

def test_range():
    result = find_multiples_of_3()
    for num in result:
        assert 1 <= num <= 1000, f"Число {num} вне диапазона 1..1000"

def test_uniqueness():
    result = find_multiples_of_3()
    assert len(result) == len(set(result)), "Есть дубликаты в списке"

def test_correct_values():
    expected = [i for i in range(1, 1001) if i % 3 == 0]
    result = find_multiples_of_3()
    assert result == expected, "Список не соответствует ожидаемому"
