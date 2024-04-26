import threading
import tkinter as tk
from turtle import width
from DisplayServiceManager import DisplayServiceManager
from ctypes import windll
from Colors import Colors
from MouseTracer import MouseTracer

class Display:
    
    TRANSPARENT_COLOR = '#60b26c'

    def __init__(self):
        # Initialize Tkinter
        self._root = tk.Tk()
        self._root.title("Robot Framework Listener")
        self._root.attributes('-alpha', 1)
        self._root.attributes('-topmost', True)
        self._root.attributes('-fullscreen', True)
        self._root.wm_attributes('-transparentcolor', Colors.TRANSPARENT_COLOR)
        
        self._screen_width = self._root.winfo_screenwidth()
        self._screen_height = self._root.winfo_screenheight()
        
        self._display_value = tk.StringVar(value="Waiting for Robot Framework execution...")
        self._keyword_label = tk.Label(
            master=self._root,
            textvariable=self._display_value,
            font=("Helvetica", 24)
        )
        self._keyword_label.pack(side=tk.LEFT, expand=False)
        self._keyword_label.bind('<Enter>', self.on_mouse_enter)
        
         # Create a canvas for drawing lines
        self._canvas = tk.Canvas(self._root, 
                                 width=self._screen_width,
                                 height=self._screen_height)
        self._mouse_tracer = MouseTracer(
            canvas=self._canvas,
            fill=Colors.TRANSPARENT_COLOR
        )
        # self._canvas.create_rectangle(0, 0, self._screen_width, self._screen_height, fill=Colors.TRANSPARENT_COLOR)
        self._canvas.pack(fill=tk.BOTH, expand=True)
        
        # Settings for line drawing
        self._line_color = "red"
        self._line_lifetime = 5000
        self._previous_x, self._previous_y = None, None
        
        # Binding mouse movement
        self._root.bind('<Motion>', self.draw_line)
        
        # Initialize gRPC service
        display_service_manager = DisplayServiceManager(self.update_display)
        self.display_service = threading.Thread(
            target=display_service_manager.start_display_service,
            daemon=True,
        )
        
        # Wait to configure the window for click-through until it's fully loaded
        self._root.after(10, lambda: self.make_click_through(self._root.winfo_id()))

    def start(self):
        self.display_service.start()
        self._root.mainloop()
        
    def make_click_through(self, hwnd):
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, -20)
        style |= 0x80000 | 0x20
        windll.user32.SetWindowLongPtrW(hwnd, -20, style)
        
    def draw_line(self, event):
        x, y = event.x, event.y
        if self._previous_x is not None and self._previous_y is not None:
            # Draw a line from the previous point to the current point
            line = self._canvas.create_line(self._previous_x, self._previous_y, x, y, fill=self._line_color)
            # Schedule the line to disappear
            self._canvas.after(self._line_lifetime, self._canvas.delete, line)
        # Update the current point
        self._previous_x, self._previous_y = x, y

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
