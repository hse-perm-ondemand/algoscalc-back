def fibonacci(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def main(n: int):
    return {"result": fibonacci(n)}


if __name__ == "__main__":
    num = 10
    print(f"n = {num}, n-е число Фибоначчи = {fibonacci(num)}")
