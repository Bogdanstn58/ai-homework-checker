// tests/test_cpp.cpp
#include <gtest/gtest.h>

// Объявляем функцию, которую тестируем (она находится в solution.cpp)
extern int sum(int a, int b);

// Тесты
TEST(SumTest, PositiveNumbers) {
    EXPECT_EQ(sum(2, 3), 5);
    EXPECT_EQ(sum(10, 20), 30);
}

TEST(SumTest, NegativeNumbers) {
    EXPECT_EQ(sum(-1, -1), -2);
    EXPECT_EQ(sum(-5, 3), -2);
}

TEST(SumTest, Zero) {
    EXPECT_EQ(sum(0, 0), 0);
    EXPECT_EQ(sum(5, 0), 5);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
