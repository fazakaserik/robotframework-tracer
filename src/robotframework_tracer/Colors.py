class Colors:
    TRANSPARENT_COLOR = "#60b26c"


class CycleColors:
    def __init__(self):
        # Define the colors of the rainbow
        self.colors = [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ]
        self.index = 0  # Initialize the index to cycle through colors

    def get_color(self):
        # Return the current color and increment the index
        color = self.colors[self.index]
        return color

    def get_next_color(self):
        # Return the current color and increment the index
        color = self.colors[self.index]
        self.index = (self.index + 1) % len(self.colors)  # Cycle the index
        return color
