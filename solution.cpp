// solution.cpp
// Задание: реализовать функцию maxMultipleOf9()
// которая возвращает максимальное число от 1 до 1000, кр

int maxMultipleOf9() {
    int max = 0;
    for (int i = 1; i <= 1000; ++i) {
        if (i % 9 == 0) {
            max = i;
        }
    }
    return max;
}
