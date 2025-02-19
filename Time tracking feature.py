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

def get_active_window_name():
    """
    Gets the name of the currently active window.
    args: none
    returns: none
    """
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
    """
    usage_data = {}
    last_app = None
    last_time = time.time()
    
    
    while True:
        # Get the currently active app and window title
        current_app, window_title = get_active_window_name()

        if current_app:
            current_time = time.time()

            # If the app changes, calculate time spent on the last app
            if last_app and current_app != last_app:
                time_spent = current_time - last_time
                usage_data[last_app] = usage_data.get(last_app, 0) + time_spent
                last_time = current_time

            last_app = current_app

        # Print usage summary every 10 seconds
        if int(current_time) % 10 == 0:
            print("\nScreen Time Summary:")
            for app, seconds in usage_data.items():
                print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")
            time.sleep(1)  # Avoid duplicate prints within the same second}
    
if __name__ == "__main__":
    track_screen_time()
