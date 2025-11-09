from typing import Self


# default to my kindle lol, paperwhite 10
class Kindle:
    def __init__(self):
        self.width: int = 600
        self.height: int = 800

    def from_dict(self, d: dict) -> Self:
        self.width = d["width"]
        self.height = d["height"]

        return self
