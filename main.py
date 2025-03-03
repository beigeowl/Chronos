import tkinter as tk
from tkinter import ttk

class createApp(tk.Tk): 
     #creates an instance of the main window as a class, creates the main application window
     #Essentially the same thing as root = tk.Tk()

    def __init__(self):    
        super().__init__() #ensures tk.Tk works properly in a class
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        

        #Main Setup
        self.title('Chronos')
        self.geometry(f'{screen_width}x{screen_height}') #Fills the window
        self.minsize(screen_width,screen_height) #Ensures window does not shrink

        #widgets
        self.menu = Menu(self)

        self.mainloop()

class Menu(ttk.Frame):
    def __init__(self, parent): 
        #Parent used to pass the newfound widget/object through the master/App
        #Creates Frame
        super().__init__(parent)
        ttk.Label(self)#.pack(expand = True, fill = 'both') # Creates Widget, comment fills the window


createApp()
