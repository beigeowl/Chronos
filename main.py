import tkinter as tk
from tkinter import ttk #Themes
from tkinter import messagebox #Pop up message windows

class createApp(tk.Tk): 
     #creates an instance of the main window as a class, creates the main application window
     #Essentially the same thing as root = tk.Tk()

    def __init__(self):    
        super().__init__() #ensures tk.Tk works properly in a class
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        #App Theme (Imported)
        self.tk.call("source", "C:/Users/benso/OneDrive/Desktop/Time Tracker App/TimeTracker/Azure-ttk-theme-main/azure.tcl") #use 'azure.tcl' when in the same file
        self.tk.call("set_theme", "dark")


        #Main Setup
        self.title('Chronos')
        self.geometry(f'{screen_width}x{screen_height}') #Fills the window
        self.minsize(int(screen_width/2),int(screen_height/2)) #Ensures window does not shrink fruther than 50% size

        #widgets
        self.menu = Menu(self)

        self.mainloop()

class Menu(ttk.Frame):
    def __init__(self, parent): 
        #Parent used to pass the newfound widget/object through the master/App
        #Creates Frame (invisible box to hold widgets)
        super().__init__(parent)
        self.place(x=0,y=0, relwidth = 1, relheight = 1)
        #x and y determine widget position, starts from top left
        #relheight and relwidth - size relative to app size

        self.create_widget()


    def create_widget(self):
        
        
        #creates widgets
        self.button1 = ttk.Button(self, text = 'show graph')
        self.menulabel = tk.Label(self, text = "Name", bg = 'red')
        self.entry = ttk.Entry(self)


        self.widget_placement() #calls placement

    def widget_placement(self):
        #create grid 2x2
        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1),weight = 1)

        #place widgets
        self.button1.grid(row = 0, column = 0)
        self.menulabel.grid(column = 0, row = 1)
        self.entry.grid(column =  1, row = 0)
createApp()


"""
with open("times.json", "r") as t:
    times = json.load(t)

daily = {key: val for key, val in sorted(times.items(), key = lambda ele: ele[1], reverse = True)}
# from https://www.geeksforgeeks.org/python-sort-a-dictionary/ 

for key, value in daily.items():

T = Text(root, height = , width = , font =, yscrollcommand = True)

T.insert()
"""
