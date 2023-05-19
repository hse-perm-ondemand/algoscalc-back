def fibonacci(n: int) -> list[int]:
    if n == 1 or n == 2:
        return [1]*n
    fibonacci_list = [1]*n
    for i in range(2, n):
        fibonacci_list[i] = fibonacci_list[i - 1] + fibonacci_list[i - 2]
    return fibonacci_list


def main(n: int):
    return {'result': fibonacci(n)}


if __name__ == '__main__':
    num = 10
    print(main(num))
