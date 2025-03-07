"""
Important message:
to use the current time tracking feature, please download the required packages time, psutil, win32gui, win32process
to install, go to command terminal and type "pip install time psutil win32gui win32process" 
program history:

"""

import time
import psutil
import win32gui
import win32process
import json


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

                with open('times.json', 'w') as fp:
                    json.dump(usage_data, fp)
                    fp.flush()
                time.sleep(1)  # Avoid duplicate prints within the same second}
    
    except KeyboardInterrupt:
        print("\nStopped Tracking")
        print("Final Screen Time Summary: ")
        for app, seconds in usage_data.items():
            print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")

track_screen_time()