# Robot Framework
from concurrent.futures import thread
import grpc
from robot.libraries.BuiltIn import BuiltIn
from robot.running.model import *

# Visual
import threading
import subprocess

import display_pb2
import display_pb2_grpc

class ListenerClass:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self._NUM_SPACES: int = 4
        self._SEPARATOR: str = ' ' * self._NUM_SPACES

        self.process = None
        self.ui_thread = threading.Thread(target=self.start_ui, daemon=True)
        self.ui_thread.start()
        
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = display_pb2_grpc.DisplayStub(self.channel)
    
    def start_ui(self):
        self.process = subprocess.Popen(["python", "Display.py"])
        
    def _display(self, text: str):
        self.stub.DisplayText(display_pb2.DisplayTextRequest(text=text))

    def start_keyword(self, data: Keyword, result):
        args_str: str = self._SEPARATOR.join(list(data.args))
        self._display(f"{data.name}{self._SEPARATOR}{args_str}")
        
    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
    