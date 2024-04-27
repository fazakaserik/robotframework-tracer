from typing import List, Optional


class CycleColors:
    _colors: List[str]
    _index: int

    def __init__(
        self,
        colors: List[str] = [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ],
    ) -> None:
        self._colors = colors
        self._index = 0
        
    # todo: color reset

    def get_color(self) -> str:
        color = self._colors[self._index]
        return color

    def get_next_color(self) -> str:
        color = self._colors[self._index]
        self.index = (self._index + 1) % len(self._colors)
        return color
