cmake_minimum_required(VERSION 3.14)
project(StudentHomework CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Добавляем исполняемый файл студента (опционально, можно и без него)
add_executable(student_solution solution.cpp)

# ---- Настройка тестов с GoogleTest ----
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
FetchContent_MakeAvailable(googletest)

# Создаём исполняемый файл для тестов
add_executable(run_tests tests/test_cpp.cpp solution.cpp)
target_link_libraries(run_tests GTest::gtest GTest::gtest_main)

# Включаем тестирование CTest
enable_testing()
add_test(NAME CppHomeworkTest COMMAND run_tests)
