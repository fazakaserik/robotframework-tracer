import threading
import tkinter as tk
from DisplayService import start_display_service

class Display:

    def __init__(self):     
        # Init TKinter
        self._root = tk.Tk()
        self._root.title("Robot Framework Listener")
        self._root.overrideredirect(True) 
        self._root.geometry(f"+0+0")
        self._root.attributes('-topmost', True)
        
        self._display_value = tk.StringVar(value="Waiting for Robot Framework execution...")
        
        self._keyword_label = tk.Label(
            master=self._root, 
            text="Waiting for Robot Framework execution...", 
            font=("Helvetica", 24),
            textvariable=self._display_value
            )
        self._keyword_label.pack(side=tk.LEFT, expand=True)
        self._keyword_label.bind('<Enter>', self.move_label_to_right)
        
        # Init gRPC service
        self.display_service = threading.Thread(
            target=start_display_service, 
            daemon=True,
            args=(self.update_display,)
            )
        
    def start(self):
        self.display_service.start()
        self._root.mainloop()
        
    def move_label_to_right(self, event):
        self._keyword_label.pack_forget() 
        self._keyword_label.pack(side=tk.RIGHT, expand=True)
        
    def update_display(self, text: str):
        self._display_value.set(text)
        self._root.update()
        

if __name__ == "__main__":
    Display().start()