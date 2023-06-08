from typing import Any


VOLUME = 'volume'
COST = 'cost'
NON_FLOAT_PARAM_TEMPL = 'Значение параметра {0} не является вещественным числом'
NEG_VALUE_PARAM_TEMPL = 'Значение параметра {0} меньше нуля'
DISTANCE_NAME = 'расстояние'
MEAN_NAME = 'средний расход'
PRICE_NAME = 'цена'


def __check_params_raises_ex(distance: float, mean_consumption: float,
                             price: float) -> None:
    str_params = [[DISTANCE_NAME, distance],
                  [MEAN_NAME, mean_consumption],
                  [PRICE_NAME, price]]
    for name, value in str_params:
        if type(value) != float:
            raise TypeError(NON_FLOAT_PARAM_TEMPL.format(name))
        if value < 0:
            raise ValueError(NEG_VALUE_PARAM_TEMPL.format(name))


def main(distance: float, mean_consumption: float, price: float,
         need_round: bool) -> dict[str, Any]:
    __check_params_raises_ex(distance, mean_consumption, price)
    volume = distance * mean_consumption / 100
    cost = volume * price
    if need_round:
        return {VOLUME: float(round(volume)), COST: float(round(cost))}
    return {VOLUME: round(volume, 2), COST: round(cost, 2)}


if __name__ == '__main__':
    print(main(100.0, 7.5, 45.0, True))
