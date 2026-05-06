// solution.cpp
int maxMultipleOf9() {
    int max = 0;
    for (int i = 1; i <= 1000; ++i) {
        if (i % 9 == 0) {
            max = i;
        }
    }
    return max;
}

// Альтернативное эффективное решение (без цикла):
int maxMultipleOf9_efficient() {
    return (1000 / 9) * 9;
}
