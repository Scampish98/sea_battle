import abc
import random
import time
import traceback

from field import Field
from ship import Ship
from point import Point


class BasePlayer(abc.ABC):
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    def __init__(self):
        self._field = Field()

    @abc.abstractmethod
    def build_field(self):
        pass

    @abc.abstractmethod
    def hit(self, other_player):
        pass

    def print_field(self):
        self._field.print()

    def print_hidden_field(self):
        self._field.print_hidden()

    def build_random_field(self):
        while True:
            try:
                self._build_random_field()
                break
            except Exception:
                self._field.clear_ships()
                time.sleep(1)

    def _build_random_field(self):
        for size, count in sorted(
            self._field.limits_ship_count_by_size.items(), reverse=True
        ):
            for _ in range(count):
                self._generate_ship(size)

    def _generate_ship(self, size):
        size -= 1
        candidates = []
        for x in range(1, self._field.width + 1):
            for y in range(1, self._field.height + 1):
                for dir in range(len(self.dx)):
                    ship = Ship(
                        Point(x, y),
                        Point(x + self.dx[dir] * size, y + self.dy[dir] * size),
                    )
                    if self._field.check_ship(ship):
                        candidates.append(ship)

        ship = random.choice(candidates)
        self._field.add_ship(ship)

    def check_hit(self, point):
        return self._field.check_hit(point)

    def take_hit(self, point):
        return self._field.hit(point)

    def check_alive_ships(self):
        return self._field.check_alive_ships()


class Player(BasePlayer):
    def __init__(self):
        super().__init__()
        self._menu = {
            "add_ship": ("добавить корабль", self._add_ship),
            "delete_ship": ("удалить корабль", self._delete_ship),
            "finish_build": ("закончить построение поля", self._finish_build),
            "build_random_field": (
                "сгенерировать поле случайным образом",
                self.build_random_field,
            ),
        }
        self._name = input("Введите свое имя: ")

    def build_field(self):
        print("Сначала необходимо расставить корабли")
        for size, limit in self._field.limits_ship_count_by_size.items():
            print(f"Кораблей размера {size} должно быть {limit}")

        while True:
            self._field.build_and_print()
            try:
                menu = [self._menu["build_random_field"]]
                if self._field.ships_count < self._field.required_ships_count:
                    menu.append(self._menu["add_ship"])
                if self._field.ships_count:
                    menu.append(self._menu["delete_ship"])
                if self._field.ships_count == self._field.required_ships_count:
                    menu.append(self._menu["finish_build"])
                menu_string = "\n".join(
                    f"{index + 1} - {item[0]}" for index, item in enumerate(menu)
                )
                select = int(input("Выберите действие\n" + menu_string + "\n")) - 1
                menu[select][1]()
            except StopIteration:
                break
            except Exception as e:
                print(traceback.print_exc())
                continue

    def _add_ship(self):
        self._field.add_ship(self._input_ship())

    def _delete_ship(self):
        self._field.delete_ship(self._input_ship())

    def _finish_build(self):
        self._field.build()
        raise StopIteration()

    def _input_ship(self):
        start = self._input_point(
            "Введите координаты начала корабля (номер строки и номер столбца): "
        )
        finish = self._input_point(
            "Введите координаты конца корабля (номер строки и номер столбца): "
        )
        return Ship(start, finish)

    def _input_point(self, message):
        return Point(
            *map(
                int,
                input(message).strip().split(),
            )
        )

    def hit(self, other_player):
        print("Ваша очередь стрелять")
        while True:
            try:
                x, y = map(int, input("Введите координаты выстрела: ").strip().split())
                result = other_player.take_hit(Point(x, y))
                print("Вы попали!" if result else "Вы промахнулись!")
                return result
            except Exception as e:
                print(e)


class AI(BasePlayer):
    def build_field(self):
        self.build_random_field()
        self._field.build()

    def hit(self, other_player):
        candidates = [
            Point(x, y)
            for x in range(1, self._field.width + 1)
            for y in range(1, self._field.height + 1)
            if other_player.check_hit(Point(x, y))
        ]
        point = random.choice(candidates)
        result = other_player.take_hit(point)
        print(f"Выстрел противника в ({point.x}, {point.y})")
        print("Попадание!" if result else "Промах!")
        return result
