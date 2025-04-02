import matplotlib.pyplot as plt
import matplotlib.animation as animation
import functools
import threading
import time
import psutil
import win32gui
import win32process
import win32api
import json
import datetime

def get_active_window_name():
    """
    Gets the name of the currently active window.
    args: none
    returns:
        description (str): the description of a .exe file (used as process "name")
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
        
        # Get the description (description gives a proper name, like "Microsoft Edge" instead of "msedge.exe")
        description = win32api.GetFileVersionInfo(exe_path, string_file_info)
        
        return description
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
    
    global weekly_data
    weekly_data = {}
    
    last_app = None
    last_time = time.time()
    
    try:
        while True:
            # Get the currently active app and window title
            current_app = get_active_window_name()
            
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

            # if new day
            if datetime.datetime.now().time().replace(second=0, microsecond=0) == datetime.time(0,0):
                weekly_data = {datetime.datetime.now().strftime('%d/%m'):sum(usage_data.values())}
                
                # save daily data to weekly.json, along with date
                with open('weekly.json', 'w') as f:
                    json.dump(weekly_data)

                # clear daily storage
                usage_data = {}
                open("daily.json", 'w').close()
    
    except KeyboardInterrupt:
        print("\nStopped Tracking")
        print("Final Screen Time Summary: ")
        for app, seconds in usage_data.items():
            print(f"{app}: {seconds // 60:.0f} min {seconds % 60:.0f} sec")

fig, ax = plt.subplots()

def plotdaily(frame, ax, usage_data):
    
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

time.sleep(1)
ani = animation.FuncAnimation(fig, functools.partial(plotdaily, ax=ax, usage_data=usage_data))
plt.show()

# with open('daily.json', 'w') as f:
#     json.dump(sum(usage_data.values()), f)
# usage_data = {}

# on program close: save daily data to json (useful when computer is shut down)
with open('daily.json', 'w') as f:
    json.dump((usage_data), f)

print("end")
