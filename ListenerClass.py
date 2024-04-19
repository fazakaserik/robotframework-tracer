# Robot Framework
from concurrent.futures import thread
from robot.libraries.BuiltIn import BuiltIn
from robot.running.model import *

# Visual
import tkinter as tk
import threading
import subprocess

from TracerLabel import TracerLabel

class ListenerClass:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self._NUM_SPACES: int = 4
        self._SEPARATOR: str = ' ' * self._NUM_SPACES

        self.process = None
        self.ui_thread = threading.Thread(target=self.start_ui, daemon=True)
        self.ui_thread.start()
    
    def start_ui(self):
        self.process = subprocess.Popen(["python", "TracerLabel.py"])
        
    def _display(self, text: str):
        pass

    def start_keyword(self, data: Keyword, result):
        args_str: str = self._SEPARATOR.join(list(data.args))
        self._display(f"{data.name}{self._SEPARATOR}{args_str}")
        
    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
    