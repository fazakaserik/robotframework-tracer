from collections import deque
from typing import Iterable, List


class CycleColors:

    def __init__(
        self,
        colors: Iterable = [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ],
    ) -> None:
        self._colors = deque(colors)

    def get_color(self) -> str:
        return self._colors[0]

    def cycle(self) -> None:
        self._colors.append(self._colors.popleft())
