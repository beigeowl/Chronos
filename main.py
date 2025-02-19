import tkinter as tk


wind = tk.Tk()
screen_width = wind.winfo_screenwidth()
screen_height = wind.winfo_screenheight()
#creates main window

wind.title("Time Tracker App")
print(screen_width, screen_height)
wind.geometry(f"{screen_width}x{screen_height}")
wind.minsize("400x400")

timer = tk.Label(wind, text=f"total time = {}", font=("Arial", 16))
timer.pack(pady=20)

def update_timer():
    timer.config(text=f"total time = {}")
    wind.after(10000,update_timer)

wind.mainloop()
