# Chronos
Lightweight, minimalistic Windows time tracking app for ICS4U SDP

# Features
Chronos takes a minimalistic approach to screen time tracking on Windows.\
It graphs and lists screen time usage per app, across a day.\
When the interface is closed, it minimizes to the system tray and continues to track screen time.

# Installation
Ensure the entire repo is downloaded, every file is necessary for program function

To run Chronos as a Python file, you'll need to create a virtual environment (venv)\
From your terminal of choice, activate the venv (https://docs.python.org/3/library/venv.html)

Run `pip install -r requirements.txt` to install all packages

## .exe compilation
If the program is to be run at startup, and as a .exe file, run `pyinstaller --onefile --windowed chronos.py` to compile the code into a .exe\
This can then be set as a startup Windows app by adding a shortcut to the .exe to the startup app folder

# Support
Developers can be reached via email:\
elu4@ocdsb.ca\
yzhao3@ocdsb.ca\
byeun3@ocdsb.ca

# Sources
[1] Real Python, "Python Thread Lock," Real Python, 2023. [Online]. Available: https://realpython.com/python-thread-lock/. [Accessed: 3-March-2025].

[2] Stack Overflow, "Protocols in Tkinter in Python," Stack Overflow, 2017. [Online]. Available: https://stackoverflow.com/questions/45726304/protocols-in-tkinter-in-python. [Accessed: 3-April-2025].

[3] Python Tutorial, "Tkinter System Tray," Python Tutorial, 2023. [Online]. Available: https://www.pythontutorial.net/tkinter/tkinter-system-tray/. [Accessed: 22-March-2025].

[4] “Developing a full tkinter object-oriented application,” Python Tutorial, https://www.pythontutorial.net/tkinter/tkinter-object-oriented-application/ (accessed Mar. 5, 2025). 

[5] Python Software Foundation, "Threading — Thread-based parallelism," Python Documentation, 2023. [Online]. Available: https://docs.python.org/3/library/threading.html. [Accessed: 7-March-2025].

[6] Stack Overflow, "Executing multiple functions simultaneously," Stack Overflow, 2013. [Online]. Available: https://stackoverflow.com/questions/18864859/executing-multiple-functions-simultaneously. [Accessed: 14-March-2025].

[7] Python GUIs, "Create UI with Tkinter Grid Layout Manager," Python GUIs, 2023. [Online]. Available: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/. [Accessed: 10-March-2025].

[8] StudyTonight, "Python Tkinter Widgets," StudyTonight, 2023. [Online]. Available: https://www.studytonight.com/tkinter/python-tkinter-widgets. [Accessed: 26-March-2025].

[9] TkDocs, "Tkinter Treeview," TkDocs, 2023. [Online]. Available: https://tkdocs.com/tutorial/tree.html. [Accessed: 9-April-2025].

[10] Dev.to, "List of Widgets in Tkinter," Dev.to, 2023. [Online]. Available: https://dev.to/shadowclaw11/list-of-widgets-in-tkinter-5b4n. [Accessed: 27-Febuary-2025].

[11] GeeksforGeeks, "Matplotlib.pyplot.tight_layout() in Python," GeeksforGeeks, 2023. [Online]. Available: https://www.geeksforgeeks.org/matplotlib-pyplot-tight_layout-in-python/. [Accessed: 15-April-2025].

[12] Ask Ubuntu, "Getting the name of the process that corresponds to the active window," Ask Ubuntu, 2012. [Online]. Available: https://askubuntu.com/questions/152191/getting-the-name-of-the-process-that-corresponds-to-the-active-window. [Accessed: 29-January-2025].

[13] psutil, "psutil documentation," psutil, 2023. [Online]. Available: https://psutil.readthedocs.io/en/latest/. [Accessed: 4-Febuary-2025].

[14] GitHub, "pywin32 Documentation," GitHub, 2023. [Online]. Available: https://github.com/mhammond/pywin32/blob/main/adodbapi/readme.txt. [Accessed: 4-Febuary-2025].

[15] Microsoft, "StringFileInfo Block," Microsoft Docs, 2023. [Online]. Available: https://learn.microsoft.com/en-us/windows/win32/menurc/stringfileinfo-block. [Accessed: 4-Febuary-2025].

[16] Stack Overflow, "How do I sort a dictionary by value?," Stack Overflow, 2009. [Online]. Available: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value. [Accessed: 1-May-2025].
