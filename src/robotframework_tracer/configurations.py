import json
from enum import Enum
from typing import Literal, LiteralString


class Configurations:

    class ExecutionTraceConfigurations:

        class Location(Enum):
            TOP_LEFT = "Top Left"
            TOP_MIDDLE = "Top Middle"
            TOP_RIGHT = "Top Right"
            BOTTOM_LEFT = "Bottom Left"
            BOTTOM_MIDDLE = "Bottom Middle"
            BOTTOM_RIGHT = "Bottom Right"

        def __init__(self, enabled: bool, location: str) -> None:
            self.enabled: bool = enabled
            self.location: type[self.Location] = self._parse_location(location)

        def _parse_location(self, location_str: str):
            """Converts a location string to a Location enum."""
            try:
                return self.Location(location_str.upper().replace(" ", "_"))
            except ValueError:
                raise ValueError(
                    f"Invalid location: {location_str}. Must be one of {[e.value for e in self.Location]}"
                )

    class MouseTraceConfigurations:
        def __init__(
            self, enabled: bool, max_mouse_clicks_recorded: int
        ) -> None:
            self.enabled: bool = enabled
            self.max_mouse_clicks_recorded: int = max_mouse_clicks_recorded

    def __init__(self, config_file):
        self._config_file = config_file
        with open(self.config_file, "r") as file:
            self._config_data = json.load(file)

        self.execution_state = self.ExecutionTraceConfigurations(
            enabled=self._config_data["executionTrace"]["enabled"],
            location=self._config_data["executionTrace"]["location"],
        )

        self.mouse_trace = self.MouseTraceConfigurations(
            enabled=self._config_data["mouseTrace"]["enabled"],
            max_mouse_clicks_recorded=self._config_data["mouseTrace"][
                "maxMouseClicksRecorded"
            ],
        )
