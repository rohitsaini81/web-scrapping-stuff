import tkinter as tk
from tkinter import ttk

# -------------------------------------------
# TEMP APP DATA (later replace with API data)
# -------------------------------------------
apps_data = [
    {"app_id": 1001, "name": "DrinkNow", "platform": "Android"},
    {"app_id": 1002, "name": "ChatTalk", "platform": "Android"},
    {"app_id": 1003, "name": "PhotoMagic", "platform": "iOS"},
    {"app_id": 1004, "name": "GameHub", "platform": "Android"},
]

import requests

response_apps = requests.get("http://localhost:5000/api/apps")
apps = response_apps.json()


# -------------------------------------------
# GUI APPLICATION
# -------------------------------------------
def main():
    root = tk.Tk()
    root.title("Apps List")
    root.geometry("600x400")

    # Title
    title = tk.Label(root, text="List of Apps", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    # Table Frame
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Treeview (Table)
    columns = ("app_id", "name", "platform")
    table = ttk.Treeview(frame, columns=columns, show="headings")

    # Column Titles
    table.heading("app_id", text="App ID")
    table.heading("name", text="Name")
    table.heading("platform", text="Platform")

    # Column Sizes
    table.column("app_id", width=100)
    table.column("name", width=250)
    table.column("platform", width=150)

    # Insert Data
    for app in apps:
        table.insert("", tk.END, values=(app["id"], app["name"], app["downloads"]))

    table.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
