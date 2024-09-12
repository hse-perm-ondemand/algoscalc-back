import copy


def __sub(n: list[list[float]], m: list[list[float]]) -> list[list[float]]:
    res: list[list[float]] = copy.deepcopy(n)
    for i in range(len(res)):
        for j in range(len(res[0])):
            res[i][j] = res[i][j] - m[i][j]
    return res


def __check_matrix(matrix: list[list[float]], name: str, row_len: int) -> None:
    for row in matrix:
        if row_len != len(row):
            raise ValueError(f"Введено неверное количество столбцов для {name}")
        for item in row:
            if item is None:
                raise ValueError(f"Не введено значение в матрице {name}")


def main(n: list[list[float]], m: list[list[float]]) -> dict[str, list[list[float]]]:
    if len(n) != len(m):
        raise ValueError("Длины матриц не совпадают!")
    dl_row = len(n[0])
    __check_matrix(n, "n", dl_row)
    __check_matrix(m, "m", dl_row)
    return {"result": __sub(n, m)}


if __name__ == "__main__":
    n = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]]
    m = [[0.0, 2.0, 2.0], [2.0, 1.0, 4.0]]
    print(__sub(n, m))
