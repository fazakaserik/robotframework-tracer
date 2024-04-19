# Robot Framework
from robot.libraries.BuiltIn import BuiltIn
from robot.running.model import *

# Visual
import tkinter as tk
import threading

class ListenerClass:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.NUM_SPACES = 4
        self.SEPARATOR = ' ' * self.NUM_SPACES

        self.root = tk.Tk()
        self.root.title("Robot Framework Listener")
        self.root.resizable(True, True)
        
        self.keyword_label = tk.Label(self.root, text="Waiting for Robot Framework execution...", font=("Helvetica", 16))
        self.keyword_label.pack(expand=True)

    def _display(self, text: str):
        self.keyword_label.config(text=text)
        self.root.update()

    def start_keyword(self, data: Keyword, result):
        args_str: str = self.SEPARATOR.join(list(data.args))
        self._display(f"{data.name}{self.SEPARATOR}{args_str}")