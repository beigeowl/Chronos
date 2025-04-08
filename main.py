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
print(usage_data)
usage_data_lock = threading.Lock()

if not(os.path.exists("daily.json")):
    print("daily.json doesn't exist, creating now")
    g = open("daily.json", "w")
    g.write("{}")
    g.close()

with open("daily.json", "r") as file:
    usage_data = json.load(file)

print(usage_data)

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

        #App Theme (Imported)
        # self.tk.call("source", "C:\\Users\\benso\\OneDrive\\Desktop\\Time Tracker App\\TimeTracker\\Azure-ttk-theme-main\\azure.tcl") #use 'azure.tcl' when in the same file
        # self.tk.call("set_theme", "dark")

    def minimize_to_tray(self):
        self.withdraw()
        image = Image.open("app.ico")
        menu = (pystray.MenuItem('Quit', self.quit_window), 
                pystray.MenuItem('Show', self.show_window))
                # ,pystray.MenuItem((f"Total: {Menu.totalTime() // 60:.0f} min {Menu.totalTime() % 60:.0f} sec"), self.e()))
        icon = pystray.Icon("name", image, "Chronos", menu)
        icon.run()

    def e(self):
        print()

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

        if not self.tracking:
            print('Tracking started!')
            self.tracking = True
            self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True)
            self.track_thread.start()

        self.create_widget()

    def create_widget(self):
        
        #Grid Configure
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 6)
        self.columnconfigure((0,1), weight=1)

        #Frames
        self.leftframe = tk.Frame(self)
        self.leftframe.grid(column = 0, row = 1)
        self.leftframe.rowconfigure((0,3), weight = 1)
        self.leftframe.columnconfigure(0, weight = 1)

        self.rightframe = tk.Frame(self)
        self.rightframe.grid(column = 1, row = 1)
        self.rightframe.rowconfigure((0,4), weight = 1)
        self.rightframe.columnconfigure(0, weight = 1)

        #Title
        self.title =  ttk.Label(self, text = 'Chronos', font = ("Helvetica", 35, "bold"))

        #Left Frame
        self.apptime = ttk.Label(self.rightframe, text = "App Time", font = ("Helvetica", 15, "bold"))
        self.totaltime = ttk.Label(self.rightframe, text = "Total Time", font = ("Helvetica", 15, "bold"))
        
        self.applist = ttk.Treeview(self.rightframe, columns = ("App", "Time"), show = 'headings', height = 16)
        self.applist.heading("App", text = "App")
        self.applist.heading("Time", text = "Time")
        self.scrollbar = ttk.Scrollbar(self.applist, orient="vertical", command=self.applist.yview)
        self.applist.configure(yscrollcommand = self.scrollbar.set)
        self.applist.columnconfigure(0, weight = 1)
        self.applist.columnconfigure(1, weight = 0)
        # self.applist.grid(column = 1 ,row = 0)
        # self.scrollbar.grid(column = 1, row = 0, sticky = "E")

        #Right Frame
        self.screentime = ttk.Label(self.leftframe, text = "Screen Time", font = ("Helvetica", 15, "bold"))
        # self.start_button = ttk.Button(self.leftframe, text='Start', command=self.start_timer)
        # self.stop_button = ttk.Button(self.leftframe, text='Stop', command=self.stop_timer)
        
        #Graph
        self.graph_frame = tk.Frame(self.leftframe)
        # self.graph_frame.grid(row=0, column=1, padx=20, pady=20)
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Time per App")
        self.ax.set_xlabel("App")
        self.ax.set_ylabel("Seconds")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()
        
        self.widget_placement()
        self.update_graph()  # Start periodic update

    def widget_placement(self):

        #Title
        self.title.grid(row = 0, columnspan = 2, sticky = 'N')

        #Left Frame
        self.apptime.grid(row = 0, column = 0, pady = 10)
        self.totaltime.grid(row = 2, column = 0,pady = 10)
        self.applist.grid(row = 1, column = 0, pady = 10)

        #Right Frame
        self.screentime.grid(row = 0, column = 0, sticky = 'N', pady = (10,0))
        self.graph_frame.grid(row = 2, column = 0, pady = 10)
        # self.start_button.grid(row=3, column=0, sticky='W', padx=10, pady=10)
        # self.stop_button.grid(row=3, column=0, sticky='E', padx=10, pady=10)
    
    def update_totaltime(self):
        currentTot = self.totalTime()
        hr = int(currentTot)//3600
        min = (int(currentTot)%3600)//60
        sec = int(currentTot)%60
        self.totaltime.config(text = f'Total Time = {hr}h {min}m {sec}s')

    def update_app_list(self):
        # Clear current list
        for item in self.applist.get_children():
            self.applist.delete(item)

        # Add current app times
        with usage_data_lock:
            for app, seconds in usage_data.items():
                hours = int(seconds)//3600
                minutes = (int(seconds)%3600) // 60
                secs = int(seconds) % 60
                formatted_time = f"{hours}h {minutes} min {secs} sec"
                self.applist.insert('', 'end', values=(app, formatted_time))

    def update_graph(self):
        self.ax.clear()
        with usage_data_lock:
            x = list(usage_data.keys())
            y = list(usage_data.values())
        bars = self.ax.bar(x, y)
        self.ax.bar_label(bars)
        self.ax.tick_params(axis='x', labelrotation=90)
        self.canvas.draw()

        #Misc Updates
        self.update_app_list()
        self.update_totaltime()

        self.after(1000, self.update_graph)

    def get_active_window_name(self):
        time.sleep(0.5)
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
    
    @staticmethod
    def totalTime():
        totalTime = sum(usage_data.values())
        return totalTime

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

                    print(f"Total: {self.totalTime() // 60:.0f} min {self.totalTime() % 60:.0f} sec")
                    time.sleep(0.5)
        except Exception as e:
            print("Exception in tracking:", e)

app = createApp()
app.mainloop()
print('done')
