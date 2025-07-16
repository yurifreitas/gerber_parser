import tkinter as tk
import time
import threading

class GerberCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.paths = []

    def load_paths(self, paths):
        self.paths = paths
        self.delete("all")
        self._desenhar_preview()

    def _desenhar_preview(self):
        last = None
        for x, y, state in self.paths:
            if state == "draw" and last:
                self.create_line(last[0]*10, last[1]*10, x*10, y*10, fill="blue")
            last = (x, y)

    def simular_trajetoria(self, paths):
        self.delete("all")
        def run():
            last = None
            for x, y, state in paths:
                if state == "draw" and last:
                    self.create_line(last[0]*10, last[1]*10, x*10, y*10, fill="red", width=2)
                    self.update()
                    time.sleep(0.05)
                last = (x, y)
        threading.Thread(target=run).start()
