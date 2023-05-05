from math import sqrt


def quadratic_equation(a: float, b: float,
                        c: float) -> str:

    if not (isinstance(a, (int, float)) and
            isinstance(b, (int, float)) and isinstance(c, (int, float))):
        raise TypeError('Коэффициенты должны быть числами')
    elif a == 0:
        raise ValueError('Коэффициент при х^2 в квадратном уравнении '
                         'не может быть равен 0!')
    else:
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return 'Действительных корней нет, т. к. D < 0'
        elif discriminant == 0:
            x = -b / (2 * a)
            if b == 0 and c == 0:
                x = abs(x)
            return 'Корень только один: x = ' + str(x)
        else:
            x1 = (-b + sqrt(discriminant)) / (2 * a)
            x2 = (-b - sqrt(discriminant)) / (2 * a)
            return 'x1 = ' + (str(round(x1, 8))) \
                   + ',' + ' x2 = ' + str((round(x2, 8)))


def main(a: float, b: float, c: float):
    return {'roots': quadratic_equation(a, b, c)}


if __name__ == '__main__':
    a = 1.0
    b = 0.0
    c = 0.0
    print(quadratic_equation(a, b, c))
