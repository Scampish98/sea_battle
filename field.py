import copy
from collections import Counter
from itertools import combinations


class Field:
    width = 6
    height = 6
    limits_ship_count_by_size = {1: 4, 2: 2, 3: 1}
    chars = {
        "ship": "■",
        "empty": "О",
        "shot": "X",
        "miss": "T",
        "hidden": "-",
    }

    def __init__(self, ships=None):
        if ships is None:
            ships = []
        for size, count in Counter(ship.size() for ship in ships):
            if count > self.limits_ship_count_by_size[size]:
                raise FieldError(
                    f"Ожидалось кораблей размера {size} не больше "
                    f"{self.limits_ship_count_by_size[size]}, "
                    f"получено: {count}"
                )
        self._ships = set(ships)
        self._field = None
        self.clear()
        self.check()

    def check_ship(self, ship):
        try:
            self.add_ship(ship)
        except Exception:
            return False
        else:
            self.delete_ship(ship)
            return True

    def add_ship(self, ship):
        if (
            self._ship_count_by_size[ship.size]
            == self.limits_ship_count_by_size[ship.size]
        ):
            raise FieldError(
                f"Превышено допустимое количество кораблей размера {ship.size}"
            )
        if ship in self._ships:
            raise FieldError(f"Такой корабль уже существует")
        self._ships.add(ship)
        try:
            self.check()
        except Exception:
            self._ships.remove(ship)
            raise

    def delete_ship(self, ship):
        if ship not in self._ships:
            raise FieldError(f"На поле нет такого корабля")
        self._ships.remove(ship)

    @property
    def _ship_count_by_size(self):
        return Counter(ship.size for ship in self._ships)

    def check(self):
        for ship in self._ships:
            for coordinate in ship.coordinates:
                if not self._check_in_field(coordinate):
                    raise FieldError("Корабль за пределами поля")
        for first, second in combinations(self._ships, 2):
            if first.distance(second) < 2:
                raise FieldError(
                    "Корабли должны находиться на расстоянии"
                    " минимум одна клетка друг от друга"
                )

    def build_and_print(self):
        self.build()
        self.print()

    def build(self):
        self.clear()
        for ship in self._ships:
            for point in ship.coordinates:
                self._field[point.x][point.y] = self.chars["ship"]

    def clear_ships(self):
        self._ships.clear()
        self.clear()

    def clear(self):
        self._field = [
            [self.chars["empty"] for _ in range(self.width + 1)]
            for _ in range(self.height + 1)
        ]

    def hit(self, point):
        if not self._check_in_field(point):
            raise HitError("Выстрел за пределы поля")
        if self._field[point.x][point.y] in (self.chars["shot"], self.chars["miss"]):
            raise HitError("Повторно стрелять в ту же клетку нельзя")
        result = self._field[point.x][point.y] == self.chars["ship"]
        self._field[point.x][point.y] = (
            self.chars["shot"] if result else self.chars["miss"]
        )
        return result

    def check_hit(self, point):
        return self._check_in_field(point) and not self._field[point.x][point.y] in (
            self.chars["shot"],
            self.chars["miss"],
        )

    def print_hidden(self):
        print_field([[self.hidden_cell(cell) for cell in row] for row in self._field])

    def hidden_cell(self, cell):
        return (
            cell
            if cell
            in (
                self.chars["shot"],
                self.chars["miss"],
            )
            else self.chars["hidden"]
        )

    def print(self):
        print_field(self._field)

    def _check_in_field(self, p):
        return 1 <= p.x <= self.width and 1 <= p.y <= self.height

    def check_alive_ships(self):
        return any(cell == self.chars["ship"] for row in self._field for cell in row)

    @property
    def required_ships_count(self):
        return sum(self.limits_ship_count_by_size.values())

    @property
    def ships_count(self):
        return len(self._ships)


def print_field(field):
    print_row(" ", (str(column_index + 1) for column_index in range(Field.width)))
    print(f"--+{'--' * Field.width}")
    for index, row in enumerate(field[1:]):
        print_row(index + 1, row[1:])


def print_row(name, row):
    print(f"{name} | {' '.join(row)}")


class FieldError(Exception):
    pass


class HitError(Exception):
    pass
