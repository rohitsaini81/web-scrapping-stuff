import tkinter as tk
from navbar import Navbar

class AppPreview:
    def __init__(self, parent, app_id, name, platform):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Preview - {name}")
        self.window.geometry("350x250")
        self.window.resizable(False, False)

        tk.Label(self.window, text="App Preview", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.window, text=f"App ID: {app_id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.window, text=f"Name: {name}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.window, text=f"Platform: {platform}", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=15)




class PreviewScreen(tk.Frame):
    def __init__(self, root, app_id, name, platform):
        super().__init__(root)
        self.root = root
        
        root.last_preview_data = (app_id, name, platform)

        tk.Label(self, text="App Preview", font=("Arial", 18, "bold")).pack(pady=15)

        tk.Label(self, text=f"App ID: {app_id}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self, text=f"Name: {name}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self, text=f"Platform: {platform}", font=("Arial", 14)).pack(pady=5)

        tk.Button(self, text="Back", command=root.show_apps_screen).pack(pady=15)
