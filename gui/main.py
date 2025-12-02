import tkinter as tk
from tkinter import ttk
from preview import PreviewScreen
import requests
from navbar import Navbar

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Apps List")
        self.geometry("700x500")

        self.current_screen = None

        # load apps from API
        response = requests.get("http://localhost:5000/api/apps")
        self.apps = response.json()
        self.navbar = Navbar(self)

        self.show_apps_screen()

    # ----------------------
    # SWITCH TO A SCREEN
    # ----------------------
    def show_screen(self, screen_class, *args):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = screen_class(self, *args)
        self.current_screen.pack(fill="both", expand=True)

    # ----------------------
    # APPS LIST SCREEN
    # ----------------------
    def show_apps_screen(self):
        self.show_screen(AppsListScreen)


# ---------------------------------------------
# Screen: LIST OF APPS
# ---------------------------------------------
class AppsListScreen(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        tk.Label(self, text="Apps List", font=("Arial", 18, "bold")).pack(pady=15)

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        columns = ("id", "name", "platform")
        self.table = ttk.Treeview(frame, columns=columns, show="headings")

        self.table.heading("id", text="App ID")
        self.table.heading("name", text="Name")
        self.table.heading("platform", text="Platform")

        self.table.column("id", width=120)
        self.table.column("name", width=260)
        self.table.column("platform", width=180)

        # Insert API Data
        for app in root.apps:
            self.table.insert("", tk.END, values=(app["id"], app["name"], app["downloads"]))

        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        # Bind row click
        self.table.bind("<ButtonRelease-1>", self.row_clicked)

    def row_clicked(self, event):
        selected = self.table.focus()
        if not selected:
            return

        values = self.table.item(selected, "values")
        app_id, name, platform = values

        # Switch to preview screen
        self.root.show_screen(PreviewScreen, app_id, name, platform)


if __name__ == "__main__":
    app = App()
    app.mainloop()
