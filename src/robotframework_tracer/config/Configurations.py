import json
import os
import tempfile
from enum import Enum
from typing import Literal, LiteralString

from robotframework_tracer.config.ExecutionTraceConfigurations import (
    ExecutionTraceConfigurations,
)
from robotframework_tracer.config.MouseTraceConfigurations import (
    MouseTraceConfigurations,
)


class Configurations:

    CONFIG_FILE_PATH = os.path.join(
        tempfile.gettempdir(), "robotframework-tracer-settings.json"
    )

    def __init__(self):
        with open(self.CONFIG_FILE_PATH, "r") as file:
            self._config_data = json.load(file)

        self.execution_trace_config = ExecutionTraceConfigurations(
            enabled=self._config_data["executionTrace"]["enabled"],
            location=self._config_data["executionTrace"]["location"],
        )

        self.mouse_trace_config = MouseTraceConfigurations(
            enabled=self._config_data["mouseTrace"]["enabled"],
            max_mouse_clicks_recorded=self._config_data["mouseTrace"][
                "maxMouseClicksRecorded"
            ],
        )
