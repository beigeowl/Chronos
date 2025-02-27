class ScreenTimeTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Time Tracker")
        self.usage_data = {}
        self.last_app = None
        self.last_time = time.time()
        
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()
        
        self.label = ttk.Label(root, text="Tracking Screen Time...", font=("Arial", 12))
        self.label.pack()
        
        self.start_tracking()
    
    def get_active_window_name(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            app_name = process.name()
            return app_name
        except Exception:
            return None
    
    def track_screen_time(self):
        while True:
            current_app = self.get_active_window_name()
            current_time = time.time()

            if current_app:
                if self.last_app and current_app != self.last_app:
                    time_spent = current_time - self.last_time
                    self.usage_data[self.last_app] = self.usage_data.get(self.last_app, 0) + time_spent
                    self.last_time = current_time
                    self.update_graph()

                self.last_app = current_app
            
            time.sleep(1)
    
    def update_graph(self):
        self.ax.clear()
        apps = list(self.usage_data.keys())
        times = [self.usage_data[app] / 60 for app in apps]
        
        self.ax.barh(apps, times, color='skyblue')
        self.ax.set_xlabel("Minutes")
        self.ax.set_ylabel("Applications")
        self.ax.set_title("Screen Time Usage")
        self.canvas.draw()
    
    def start_tracking(self):
        tracking_thread = threading.Thread(target=self.track_screen_time, daemon=True)
        tracking_thread.start()
