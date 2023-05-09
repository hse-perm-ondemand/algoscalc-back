import copy


def sub(n: list[list[float]], m: list[list[float]]) -> list[list[float]]:
    res: list[list[float]] = copy.deepcopy(n)
    for i in range(len(res)):
        for j in range(len(res[0])):
            res[i][j] = res[i][j] - m[i][j]
    return res


def main(n: list[list[float]], m: list[list[float]]) -> \
        dict[str, list[list[float]]]:
    if len(n) != len(m):
        raise ValueError('Длины матриц не совпадают!')
    dl_row = len(n[0])
    for row in n:
        if dl_row != len(row):
            raise ValueError('Введено неверное количество столбовцов для n')
        for item in row:
            if item is None:
                raise ValueError('Не введено значение в матрице n')
    for row in m:
        if dl_row != len(row):
            raise ValueError('Введено неверное количество столбовцов для m')
        for item in row:
            if item is None:
                raise ValueError('Не введено значение в матрице m')
    return {'result': sub(n, m)}


if __name__ == '__main__':
    n = [[1., 2., 3.],
         [2., 3., 4.]]
    m = [[0., 2., 2.],
         [2., 1., 4.]]
    print(sub(n, m))
