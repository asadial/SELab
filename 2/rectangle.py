from .shape import Shape


class Rectangle(Shape):
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width

    def compute_area(self) -> int:
        return self.height * self.width

    def set_height(self, new_height: int) -> None:
        self.height = new_height

    def get_height(self) -> int:
        return self.height

    def set_width(self, new_width: int) -> None:
        self.width = new_width

    def get_width(self) -> int:
        return self.width
