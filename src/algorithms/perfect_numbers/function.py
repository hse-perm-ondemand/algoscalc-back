from typing import Any

from src.internal.errors import AlgorithmTypeError, AlgorithmValueError

HAS_PERFECT = "has_perfect"
PERFECT_NUMBERS = "perfect_numbers"


def __is_perfect(number: int) -> bool:
    if number in [0, 1]:
        return False
    factors = []
    for i in range(1, number - 1):
        if number % i == 0:
            factors.append(i)
    return sum(factors) == number


def __check_numbers_raises_ex(numbers: list[int]) -> None:
    if not isinstance(numbers, list):
        raise AlgorithmTypeError("Параметр не является списком")
    if len(numbers) == 0:
        raise AlgorithmValueError("Список чисел пуст")
    for val in numbers:
        if not isinstance(val, int):
            raise AlgorithmValueError("Список чисел содержит нечисловое значение")
        if val < 0:
            raise AlgorithmValueError("Список чисел содержит отрицательное значение")


def main(numbers: list[int]) -> dict[str, Any]:
    __check_numbers_raises_ex(numbers)
    perfect_numbers = list(filter(__is_perfect, numbers))
    return {HAS_PERFECT: len(perfect_numbers) > 0, PERFECT_NUMBERS: perfect_numbers}


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6]
    print(main(numbers))
