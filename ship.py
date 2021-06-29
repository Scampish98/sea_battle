from point import Point


class Ship:
    def __init__(self, start, finish):
        if start.x != finish.x and start.y != finish.y:
            raise ShipError(
                "Корабль должен быть расположен по вертикали или горизонтали"
            )

        if not 0 <= abs(start.x - finish.x) + abs(start.y - finish.y) <= 2:
            raise ShipError("Размер корабля должен быть от 1 до 3")

        if start.x > finish.x or start.y > finish.y:
            start, finish = finish, start

        self.start = start
        self.finish = finish

    @property
    def size(self):
        return abs(self.start.x - self.finish.x) + abs(self.start.y - self.finish.y) + 1

    @property
    def coordinates(self):
        if self.start.x == self.finish.x:
            return [
                Point(self.start.x, y) for y in range(self.start.y, self.finish.y + 1)
            ]
        return [Point(x, self.start.y) for x in range(self.start.x, self.finish.x + 1)]

    def distance(self, ship):
        return min(
            first_coordinate.distance(second_coordinate)
            for first_coordinate in self.coordinates
            for second_coordinate in ship.coordinates
        )

    def __hash__(self):
        return hash((self.start.x, self.start.y, self.finish.x, self.finish.y))

    def __eq__(self, other):
        return self.start == other.start and self.finish == other.finish

    def __str__(self):
        return f"Ship[start{self.start}, finish{self.finish}]"


class ShipError(Exception):
    pass
