from robotframework_tracer.config.types.Location import Location


class ExecutionTraceConfigurations:

    def __init__(self, enabled: bool, location: str) -> None:
        self.enabled: bool = enabled
        self.location: type[self.Location] = self._parse_location(location)

    def _parse_location(self, location_str: str):
        """Converts a location string to a Location enum."""
        try:
            return Location(location_str)
        except ValueError:
            raise ValueError(
                f"Invalid location: {location_str}. Must be one of {[e.value for e in Location]}"
            )
