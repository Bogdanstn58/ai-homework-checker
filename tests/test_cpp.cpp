// tests/test_cpp.cpp
#include <gtest/gtest.h>

// Объявляем функцию, которую студент должен реализовать в solution.cpp
// Она должна возвращать максимальное целое число в диапазоне [1, 1000], кратное 9.
extern int maxMultipleOf9();

// Тест: проверяем, что результат кратен 9
TEST(MaxMultipleOf9Test, IsMultipleOf9) {
    int result = maxMultipleOf9();
    EXPECT_EQ(result % 9, 0) << "Результат " << result << " не кратен 9";
}

// Тест: результат не должен превышать 1000
TEST(MaxMultipleOf9Test, NotExceeds1000) {
    int result = maxMultipleOf9();
    EXPECT_LE(result, 1000) << "Результат " << result << " больше 1000";
}

// Тест: результат должен быть положительным
TEST(MaxMultipleOf9Test, Positive) {
    int result = maxMultipleOf9();
    EXPECT_GT(result, 0) << "Результат " << result << " не положительный";
}

// Тест: максимальное число, кратное 9, в диапазоне 1..1000 — это 999
TEST(MaxMultipleOf9Test, CorrectValue) {
    int result = maxMultipleOf9();
    EXPECT_EQ(result, 999) << "Ожидалось 999, получено " << result;
}

// Дополнительный тест: убеждаемся, что нет числа больше 999 и кратного 9
TEST(MaxMultipleOf9Test, IsMaximal) {
    int result = maxMultipleOf9();
    // Проверяем, что следующее возможное кратное (result + 9) уже больше 1000
    EXPECT_GT(result + 9, 1000) << "Существует большее число, кратное 9: " << (result + 9);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
