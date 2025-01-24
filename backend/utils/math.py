from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int

    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)

    def __hash__(self):
        return hash((self.x, self.y))
