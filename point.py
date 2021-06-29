import attr


@attr.s(frozen=True, auto_attribs=True)
class Point:
    x: int
    y: int

    def distance(self, p):
        return max(abs(self.x - p.x), abs(self.y - p.y))

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"
