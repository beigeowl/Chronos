import json
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

with open("times.json", "r") as t:
    data = json.load(t)
class ScreenTimeTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Time Tracker")
        self.usage_data = data
        
        
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()
        
        self.label = ttk.Label(root, text="Tracking Screen Time...", font=("Arial", 12))
        self.label.pack()
        
        self.start_tracking()
    
    def update_graph(self):
        self.ax.clear()
        apps = list(self.usage_data.keys())
        times = [self.usage_data[app] / 60 for app in apps]
        
        self.ax.barh(apps, times, color='skyblue')
        self.ax.set_xlabel("Minutes")
        self.ax.set_ylabel("Applications")
        self.ax.set_title("Screen Time Usage")
        self.canvas.draw()
    
    def start_tracking(self):
        tracking_thread = threading.Thread(target=self.track_screen_time, daemon=True)
        tracking_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTimeTracker(root)
    root.mainloop()

