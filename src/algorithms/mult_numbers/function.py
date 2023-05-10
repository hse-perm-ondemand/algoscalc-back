
def mult_numbers(a: float, b: float) -> float:

    if not (isinstance(a, (int, float)) and
            isinstance(b, (int, float))):
        raise TypeError('Перемножать можно только числа')
    return a * b


def main(a: float, b: float):
    return {'mult': mult_numbers(a, b)}


if __name__ == '__main__':
    a = 1.0
    b = 0.0
    print(mult_numbers(a, b))
