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
import datetime

# Global data and lock for thread safety: there are 2 threads accessing usage_data at the same time which can cause errors without the lock https://realpython.com/python-thread-lock/
usage_data = {}
print(usage_data)
usage_data_lock = threading.Lock()

# creates necessary files if they don't exist
if not(os.path.exists("daily.json")):
    print("daily.json doesn't exist, creating now")
    g = open("daily.json", "w")
    g.write("{}")
    g.close()

if not(os.path.exists("date.txt")):
    print("date.txt doesn't exist, creating new")
    with open("date.txt", "w") as f:
        f.write(f"{datetime.date.today()}")
        f.close()

# clears the saved time if it is a new day. If not a new day, the saved times are loaded into the program
with open("date.txt", "r") as h:
    saved_date = h.readline()
    h.close()

if saved_date == str(datetime.date.today()):
    with open("daily.json", "r") as file:
        usage_data = json.load(file)
        file.close()

print(usage_data)

# creates the window for the app
class createApp(tk.Tk):
    def __init__(self):
        #Uses super().__init__() to ensure that other classes can inherit from the parent class, as Tkinter uses a hierarchy based system
        super().__init__()
        
        #assigning attributes to the program: Title, Startup size, State
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.title('Chronos')
        self.geometry(f'{screen_width}x{screen_height}')
        self.state('zoomed')
        self.minsize(int(screen_width/2), int(screen_height/2))
        self.menu = Menu(self)
        
        # when the x is clicked to close the window, it triggers a function instead (minimizes to tray) https://stackoverflow.com/questions/45726304/protocols-in-tkinter-in-python
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    # When the app is minimized to the tray, it can either be fully exited by clicking quit or be shown again. https://www.pythontutorial.net/tkinter/tkinter-system-tray/
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

    # when the app is fully exited, it dumps the screen time data, as well as the date
    def onExit(self):
        with open('daily.json', 'w') as f:
            json.dump((usage_data), f)
            f.close()

        with open('date.txt', 'w') as g:
            g.write(f"{datetime.date.today()}")
            g.close()
        os._exit(0)

#A menu class that inherits from the parent class, essentially oversees the entirety of everything that occurs inside the tkinter window ,https://www.youtube.com/watch?v=eaxPK9VIkFM
class Menu(ttk.Frame):
    def __init__(self, parent):
        self.tracking = False
        super().__init__(parent)

        #Establishes a 2d plane from the top left to organize and allow for widget placement
        self.place(x=0, y=0, relwidth=1, relheight=1)

        # starts the screen time tracking when the app is opened
        if not self.tracking:
            print('Tracking started!')
            self.tracking = True
            
            # creates a separate thread for the tracking such that the graph and the tracking can occur and update simultaneously https://docs.python.org/3/library/threading.html, https://stackoverflow.com/questions/18864859/executing-multiple-functions-simultaneously
            self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True)
            self.track_thread.start()

        self.create_widget()

    #Initializes the widgets in one function, assigning its attrubutes except for its location
    def create_widget(self):
        
        #Grid Configure, Organizes the 2d plane, making it a 2 x 2 grid, the 2nd row having a greater size, https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 6)
        self.columnconfigure((0,1), weight=1)

        #FRAMES, initializing frames into the following grid boxes (0,1), (1,1), for further and more precise widget placement, frames are widgets themselves, however they can be treated like a mini window

        #Left Frame, set up for further grid placement within the frame, 1 x 3, https://www.studytonight.com/tkinter/python-tkinter-widgets
        self.leftframe = tk.Frame(self)
        self.leftframe.grid(column = 0, row = 1)
        self.leftframe.rowconfigure((0,3), weight = 1)
        self.leftframe.columnconfigure(0, weight = 1)

        #Right Frame, set up for further grid placement within the frame, 1 x 5, https://www.studytonight.com/tkinter/python-tkinter-widgets
        self.rightframe = tk.Frame(self)
        self.rightframe.grid(column = 1, row = 1)
        self.rightframe.rowconfigure((0,4), weight = 1)
        self.rightframe.columnconfigure(0, weight = 1)

        #Title, with assigned attributes, https://www.studytonight.com/tkinter/python-tkinter-widgets
        self.title =  ttk.Label(self, text = 'Chronos', font = ("Helvetica", 35, "bold"))

        #Left Frame Widgets, https://www.studytonight.com/tkinter/python-tkinter-widgets
        self.apptime = ttk.Label(self.rightframe, text = "App Time", font = ("Helvetica", 15, "bold"))
        self.totaltime = ttk.Label(self.rightframe, text = "Total Time", font = ("Helvetica", 15, "bold"))
        #Attributes for the list (Treeview) including headings and size, https://tkdocs.com/tutorial/tree.html
        self.applist = ttk.Treeview(self.rightframe, columns = ("App", "Time"), show = 'headings', height = 16)
        self.applist.heading("App", text = "App")
        self.applist.heading("Time", text = "Time")
        self.scrollbar = ttk.Scrollbar(self.applist, orient="vertical", command=self.applist.yview)
        self.applist.configure(yscrollcommand = self.scrollbar.set)
        self.applist.columnconfigure(0, weight = 1)
        self.applist.columnconfigure(1, weight = 0)

        #Right Frame Widgets, https://dev.to/shadowclaw11/list-of-widgets-in-tkinter-5b4n?comments_sort=latest
        self.screentime = ttk.Label(self.leftframe, text = "Screen Time", font = ("Helvetica", 15, "bold"))
        
        #Graph
        self.graph_frame = tk.Frame(self.leftframe)
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Time per App")
        self.ax.set_xlabel("App")
        self.ax.set_ylabel("Seconds")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()
        
        self.widget_placement() # Calls to place the widgets
        self.update_graph()  # Start periodic update

    #determining coordinate placement for each widget, https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/
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

    #Updating total time, enabling for the xh ym zs format
    def update_totaltime(self):
        currentTot = self.totalTime()
        hr = int(currentTot)//3600
        min = (int(currentTot)%3600)//60
        sec = int(currentTot)%60
        self.totaltime.config(text = f'Total Time = {hr}h {min}m {sec}s')

    #Updating table times
    def update_app_list(self):
        # Clear current list
        for item in self.applist.get_children():
            self.applist.delete(item)

        # Add current app times, xh ym zs
        with usage_data_lock:
            S_usage_data = dict(sorted(usage_data.items(), key=lambda item: item[1], reverse=True))# taken from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
            for app, seconds in S_usage_data.items():
                hours = int(seconds)//3600
                minutes = (int(seconds)%3600) // 60
                secs = int(seconds) % 60
                formatted_time = f"{hours}h {minutes} min {secs} sec"
                self.applist.insert('', 'end', values=(app, formatted_time))

    # redraws the graph every second
    def update_graph(self):
        self.ax.clear()
        S_usage_data = dict(sorted(usage_data.items(), key=lambda item: item[1], reverse=True))
        with usage_data_lock:
            x = list(S_usage_data.keys())
            y = list(S_usage_data.values())
        bars = self.ax.bar(x, y)
        self.ax.tick_params(axis='x', labelrotation=90)
        plt.tight_layout()
        self.canvas.draw()

        #Misc Updates, to ensure consistent pacing across all updates
        self.update_app_list()
        self.update_totaltime()

        self.after(1000, self.update_graph)

    # https://askubuntu.com/questions/152191/getting-the-name-of-the-process-that-corresponds-to-the-active-window, https://psutil.readthedocs.io/en/latest/, https://github.com/mhammond/pywin32/blob/main/adodbapi/readme.txt
    def get_active_window_name(self):
        # gets the active window handle
        hwnd = win32gui.GetForegroundWindow()
        # get the PID of the active window
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            exe_path = proc.exe()
        except Exception:
            # could not even get a process – fallback to window title
            return win32gui.GetWindowText(hwnd) or None

        # try to get the FileDescription of a processhttps://learn.microsoft.com/en-us/windows/win32/menurc/stringfileinfo-block
        # this gives the most user friendly name for a given process. For example, for microsoft edge, it'll show "Microsoft Edge", while the process name gives "msedge" or "msedge.exe" and the window title includes the name of the active tab
        try:
            # get the list of (lang, codepage) tuples
            trans = win32api.GetFileVersionInfo(exe_path, '\\VarFileInfo\\Translation')
            lang, codepage = trans[0]
            str_path = f'\\StringFileInfo\\{lang:04x}{codepage:04x}\\FileDescription'
            desc = win32api.GetFileVersionInfo(exe_path, str_path)
            if desc and desc.strip():
                return desc
        except Exception as e:
            # catch the 1813 or any other version‑info error
            pass

        # Fallback to process name (without .exe)
        try:
            return os.path.splitext(proc.name())[0]
        except Exception:
            # last fallback: window title
            return win32gui.GetWindowText(hwnd) or None
    
    @staticmethod
    def totalTime():
        totalTime = sum(usage_data.values())
        return totalTime

    def track_screen_time(self):      
        last_app = None
        last_time = time.time()
        try:
            while self.tracking:                
                # current app is defined by the name of the active window whether that be the file description, process name, or window title
                current_app = self.get_active_window_name()
                current_time = time.time()
                if current_app:
                    if last_app is not None:
                        time_spent = round(current_time - last_time, 0)
                        with usage_data_lock:
                            usage_data[last_app] = usage_data.get(last_app, 0) + time_spent
                    last_time = current_time
                    last_app = current_app

                # print the summary
                with usage_data_lock:
                    print("\nScreen Time Summary:")
                    for app, seconds in usage_data.items():
                        print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")

                    print(f"Total: {self.totalTime() // 60:.0f} min {self.totalTime() % 60:.0f} sec")
                time.sleep(1) 

                # if the time is 00:00 system time (new day)
                if datetime.datetime.now().time().replace(second=0, microsecond=0) == datetime.time(0,0):

                    print("new day")
                    # clear the existing dict in place
                    with usage_data_lock:
                        usage_data.clear()

                    # persist the empty state
                    with open("daily.json", "w") as g:
                        json.dump({}, g)
                        g.close()

                    # update the date
                    with open('date.txt', 'w') as j:
                        j.write(f"{datetime.date.today()}")
                        j.close()
                   
        except Exception as e:
            print("Exception in tracking:", e)

app = createApp()
app.mainloop()
