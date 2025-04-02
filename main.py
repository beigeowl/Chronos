import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import functools
import threading
import time
import psutil
import win32gui
import win32process
import win32api
import sys

global usage_data
usage_data = {}
class createApp(tk.Tk): 
     #creates an instance of the main window as a class, creates the main application window
     #Essentially the same thing as root = tk.Tk()

    def __init__(self):    
        super().__init__() #ensures tk.Tk works properly in a class
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        #App Theme (Imported)
        #self.tk.call("source", "C:/Users/benso/OneDrive/Desktop/Time Tracker App/TimeTracker/Azure-ttk-theme-main/azure.tcl") #use 'azure.tcl' when in the same file
        #self.tk.call("set_theme", "dark")


        #Main Setup
        self.title('Chronos')
        self.geometry(f'{screen_width}x{screen_height}') #Sets window starting size
        self.state('zoomed') #Fills the window
        self.minsize(int(screen_width/2),int(screen_height/2)) #Ensures window does not shrink fruther than 50% size

        #widgets
        self.menu = Menu(self)

        self.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        sys.exit()

        
        

class Menu(ttk.Frame):
    def __init__(self, parent): 

        self.tracking = False

        #Parent used to pass the newfound widget/object through the master/App
        #Creates Frame (invisible box to hold widgets)
        super().__init__(parent)
        self.place(x=0,y=0, relwidth = 1, relheight = 1)
        #x and y determine widget position, starts from top left
        #relheight and relwidth - size relative to app size
        self.usage_data = {}
        self.create_widget()


    # def process_widget(self, event):
    #     print('poop')

    def create_widget(self):
        
        
        #creates widgets
        self.start_button = ttk.Button(self, text = 'start', command = self.start_timer)
        self.stop_button = ttk.Button(self, text = 'stop', command = self.stop_timer)
        self.menulabel = tk.Label(self, text = "Name", bg = 'red')
        
        self.entry = ttk.Entry(self, textvariable = 'subname')
        # self.entry.bind('<return>', self.process_widget)
        self.graph_frame = tk.Frame(self, width = 500, height = 300)
        self.graph_frame.grid(row=0, column = 1, padx = 20, pady=20)
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Time per App")
        self.ax.set_xlabel("App")
        self.ax.set_ylabel("Seconds")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

        self.widget_placement() #calls placement
        
    
        # Start animation properly
        self.ani = animation.FuncAnimation(self.fig, self.plot, interval=1000)

        # Force an initial draw
        self.canvas.draw()
    def widget_placement(self):
        #create grid 2x2
        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1),weight = 1)

        #place widgets
        self.graph_frame.grid(row = 0, column = 0, sticky = "W")
        self.start_button.grid(row = 0, column = 0, sticky = 'N')
        self.stop_button.grid(row = 0, column = 0, sticky = 'S')
        self.menulabel.grid(column = 0, row = 1, columnspan = 2)
        self.entry.grid(column =  1, row = 0)

    def start_timer(self):
        
        if not self.tracking:
            print('success!')
            self.tracking = True
            self.track_thread = threading.Thread(target=self.track_screen_time, daemon=True) #tracking screen time in the background
            self.track_thread.start()

    def stop_timer(self):
        print('stopped tracking')
        self.tracking = False

    def get_active_window_name(self):
        """
        Gets the name of the currently active window.
        args: none
        returns: none
        """
        time.sleep(1)
        try:
            hwnd = win32gui.GetForegroundWindow()  # Get the handle of the active window
            _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get the process ID
            # Get the process executable path using psutil
            process = psutil.Process(pid)
            exe_path = process.exe()
            
            # Get file info
            language, codepage = win32api.GetFileVersionInfo(exe_path, '\\VarFileInfo\\Translation')[0]
            string_file_info = f'\\StringFileInfo\\{language:04x}{codepage:04x}\\FileDescription'
            
            # Get the description
            description = win32api.GetFileVersionInfo(exe_path, string_file_info)
            
            return description
        except Exception:
            return None, None  # Return None if there's an issue
    def plot(self, frame):
        self.ax.clear()
        x = usage_data.keys()
        y = usage_data.values()
        bars = self.ax.bar(x, y)
        self.ax.bar_label(bars)
        self.canvas.draw() 
     
    def track_screen_time(self):
        """
        Tracks screen time for each app and prints the usage summary.
        args: none
        returns:
            app (string): name of a tracked app
            seconds (int): number of seconds an app has been open for
        """
        
        
        last_app = None
        last_time = time.time()
        
        try:
            while self.tracking:
                # Get the currently active app and window title
                current_app = self.get_active_window_name()
                
                if current_app:
                    current_time = time.time()

                    if int(current_time) % 2 == 0:
                        time_spent = round(current_time - last_time, 0)
                        usage_data[last_app] = usage_data.get(last_app, 0) + time_spent
                        last_time = current_time

                    last_app = current_app

                # Print usage summary every 10 seconds
                if int(current_time) % 2 == 0:
                    print("\nScreen Time Summary:")
                    for app, seconds in usage_data.items():
                        print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")

                    time.sleep(1)  # Avoid duplicate prints within the same second}
        except Exception:
            if self.tracking:
                print("\nStopped Tracking")
                print("Final Screen Time Summary: ")
                for app, seconds in usage_data.items():
                    print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")


app = createApp()
app.mainloop()
print('done')
