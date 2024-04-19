import threading
import tkinter as tk
from DisplayServiceManager import DisplayServiceManager

class Display:

    def __init__(self):
        # Initialize Tkinter
        self._root = tk.Tk()
        self._root.title("Robot Framework Listener")
        self._root.overrideredirect(True)
        self._root.geometry("+0+0")
        self._root.attributes('-topmost', True)

        self._display_value = tk.StringVar(value="Waiting for Robot Framework execution...")
        self._keyword_label = tk.Label(
            master=self._root,
            textvariable=self._display_value,
            font=("Helvetica", 24)
        )
        self._keyword_label.pack(side=tk.LEFT, expand=True)
        self._keyword_label.bind('<Enter>', self.on_mouse_enter)
        
        # Initialize gRPC service
        display_service_manager = DisplayServiceManager(self.update_display)
        self.display_service = threading.Thread(
            target=display_service_manager.start_display_service,
            daemon=True,
        )

    def start(self):
        self.display_service.start()
        self._root.mainloop()

    def update_display(self, text: str):
        self._root.after(0, self._display, text)

    def _display(self, text: str):
        self._display_value.set(text)
        self._root.update()

    def on_mouse_enter(self, event):
        pos = self._root.geometry().split('+')
        x, y = int(pos[1]), int(pos[2])
        
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()

        if x == 0 and y == 0:
            # Move from top-left to bottom of the screen
            new_y = screen_height - self._root.winfo_height()
            self._root.geometry(f"+0+{new_y}")
        else:
            # Move from bottom back to top-left
            self._root.geometry("+0+0")

# Gets called by listener
if __name__ == "__main__":
    display = Display()
    display.start()
