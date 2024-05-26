# Robot Framework
# Visual
import os
import subprocess
import sys
import threading
from concurrent.futures import thread

import grpc
from robot.running.model import Keyword

from robotframework_tracer.config.Configurations import Configurations
from robotframework_tracer.ui.generated.display_pb2 import DisplayTextRequest
from robotframework_tracer.ui.generated.display_pb2_grpc import (
    DisplayServiceStub,
)


class Listener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self._NUM_SPACES: int = 4
        self._SEPARATOR: str = " " * self._NUM_SPACES

        self.process = None
        self.config = Configurations()

        try:
            self.ui_thread = threading.Thread(target=self.start_ui, daemon=True)
            self.ui_thread.start()

            self.channel = grpc.insecure_channel("localhost:50051")
            self.stub = DisplayServiceStub(self.channel)
        finally:
            self.close()

    def start_ui(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.process = subprocess.Popen(
            [sys.executable, os.path.join(dir_path, "ui", "Display.py")]
        )

    def _display(self, text: str):
        if not self.config.execution_trace_config.enabled:
            return
        self.stub.DisplayText(DisplayTextRequest(text=text))

    def start_keyword(self, data: Keyword, result):
        args_str: str = self._SEPARATOR.join(list(data.args))
        self._display(f"{data.name}{self._SEPARATOR}{args_str}")

    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
