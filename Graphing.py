import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import functools
#import numpy as np
import threading
#import TimeTracker
import time
import psutil
import win32gui
import win32process



def get_active_window_name():
    """
    Gets the name of the currently active window.
    args: none
    returns: none
    """
    time.sleep(1)
    try:
        hwnd = win32gui.GetForegroundWindow()  # Get the handle of the active window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get the process ID
        process = psutil.Process(pid)  # Get the process object
        app_name = process.name()  # Get the process name
        window_title = win32gui.GetWindowText(hwnd)  # Get the window title
        return app_name, window_title
    except Exception:
        return None, None  # Return None if there's an issue

def track_screen_time():
    """
    Tracks screen time for each app and prints the usage summary.
    args: none
    returns:
        app (string): name of a tracked app
        seconds (int): number of seconds an app has been open for
    """
    global usage_data
    usage_data = {}
    
    last_app = None
    last_time = time.time()
    
    try:
        while True:
            # Get the currently active app and window title
            current_app, window_title = get_active_window_name()
            
            if current_app:
                current_time = time.time()

                if int(current_time) % 2 == 0:
                    time_spent = current_time - last_time
                    usage_data[last_app] = usage_data.get(last_app, 0) + time_spent
                    last_time = current_time

                last_app = current_app

            # Print usage summary every 10 seconds
            if int(current_time) % 2 == 0:
                print("\nScreen Time Summary:")
                for app, seconds in usage_data.items():
                    print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")

                # with open('times.json', 'w') as fp:
                #     json.dump(usage_data, fp)
                #     fp.flush()
                time.sleep(1)  # Avoid duplicate prints within the same second}
    
    except KeyboardInterrupt:
        print("\nStopped Tracking")
        print("Final Screen Time Summary: ")
        for app, seconds in usage_data.items():
            print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")







fig, ax = plt.subplots()

def plot(frame, ax, usage_data):
    # with open('times.json', 'r') as times:
    #     usage_data = json.load(times)

    x = usage_data.keys()
    y = usage_data.values()

    ax.clear()
    ax.bar(x,y)
    
    #extras
    ax.set_title("Time per App")
    ax.set_xlabel("App")
    ax.set_ylabel("Seconds")
    bars=ax.bar(x,y)
    ax.bar_label(bars)

timeTrackingThread = threading.Thread(target=track_screen_time, daemon = True)
timeTrackingThread.start()
ani = animation.FuncAnimation(fig, functools.partial(plot, ax=ax, usage_data=usage_data))
plt.show()
