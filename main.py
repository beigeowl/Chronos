import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import psutil
import win32gui
import win32process
import win32api
import os
import pystray
from PIL import Image
import json

# Global data and lock for thread safety
usage_data = {}
usage_data_lock = threading.Lock()

with open("daily.json", "r") as file:
    usage_data = json.load(file)

class createApp(tk.Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.title('Chronos')
        self.geometry(f'{screen_width}x{screen_height}')
        self.state('zoomed')
        self.minsize(int(screen_width/2), int(screen_height/2))
        self.menu = Menu(self)
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def minimize_to_tray(self):
        self.withdraw()
        image = Image.open("app.ico")
        menu = (pystray.MenuItem('Quit', self.quit_window), 
                pystray.MenuItem('Show', self.show_window))
        icon = pystray.Icon("name", image, "Chronos", menu)
        icon.run()

    def quit_window(self, icon):
        self.onExit()
        #os._exit(0)
        icon.stop()
        self.destroy()
        
    def show_window(self, icon):
        icon.stop()
        self.after(0,self.deiconify)

    def onExit(self):
        with open('daily.json', 'w') as f:
            json.dump((usage_data), f)
        os._exit(0)

class Menu(ttk.Frame):
    def __init__(self, parent):
        self.tracking = False
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widget()

    def create_widget(self):
        self.start_button = ttk.Button(self, text='start', command=self.start_timer)
        self.stop_button = ttk.Button(self, text='stop', command=self.stop_timer)
        self.menulabel = tk.Label(self, text="Name", bg='red')
        self.entry = ttk.Entry(self)
        self.graph_frame = tk.Frame(self, width=500, height=300)
        self.graph_frame.grid(row=0, column=1, padx=20, pady=20)
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Time per App")
        self.ax.set_xlabel("App")
        self.ax.set_ylabel("Seconds")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()
        self.widget_placement()
        self.update_graph()  # Start periodic update

    def widget_placement(self):
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        self.graph_frame.grid(row=0, column=0, sticky="W")
        self.start_button.grid(row=0, column=0, sticky='N')
        self.stop_button.grid(row=0, column=0, sticky='S')
        self.menulabel.grid(column=0, row=1, columnspan=2)
        self.entry.grid(column=1, row=0)

    def update_graph(self):
        self.ax.clear()
        with usage_data_lock:
            x = list(usage_data.keys())
            y = list(usage_data.values())
        bars = self.ax.bar(x, y)
        self.ax.bar_label(bars)
        self.canvas.draw()
        self.after(1000, self.update_graph)

    def start_timer(self):
        if not self.tracking:
            print('Tracking started!')
            self.tracking = True
            self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True)
            self.track_thread.start()

    def stop_timer(self):
        print('Stopped tracking')
        self.tracking = False

    def get_active_window_name(self):
        time.sleep(1)
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            exe_path = process.exe()
            language, codepage = win32api.GetFileVersionInfo(exe_path, '\\VarFileInfo\\Translation')[0]
            string_file_info = f'\\StringFileInfo\\{language:04x}{codepage:04x}\\FileDescription'
            description = win32api.GetFileVersionInfo(exe_path, string_file_info)
            return description
        except Exception:
            return None

    def track_screen_time(self):      
        last_app = None
        last_time = time.time()
        try:
            while self.tracking:
                current_app = self.get_active_window_name()
                current_time = time.time()
                if current_app:
                    if last_app is not None:
                        time_spent = round(current_time - last_time, 0)
                        with usage_data_lock:
                            usage_data[last_app] = usage_data.get(last_app, 0) + time_spent
                    last_time = current_time
                    last_app = current_app

                # Optional: print the summary
                with usage_data_lock:
                    print("\nScreen Time Summary:")
                    for app, seconds in usage_data.items():
                        print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")
                time.sleep(1)
        except Exception as e:
            print("Exception in tracking:", e)

app = createApp()
app.mainloop()
print('done')
