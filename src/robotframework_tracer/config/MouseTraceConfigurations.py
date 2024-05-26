class MouseTraceConfigurations:
    def __init__(self, enabled: bool, max_mouse_clicks_recorded: int) -> None:
        self.enabled: bool = enabled
        self.max_mouse_clicks_recorded: int = max_mouse_clicks_recorded
