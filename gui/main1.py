import tkinter as tk
from tkinter import ttk
from preview import AppPreview
import requests


# Load apps via API
response = requests.get("http://localhost:5000/api/apps")
apps = response.json()


def on_row_click(event):
    selected_item = table.focus()
    if not selected_item:
        return

    values = table.item(selected_item, "values")
    app_id = values[0]        # First column value
    name = values[1]
    platform = values[2]

    # Open preview window (from separate file)
    AppPreview(root, app_id, name, platform)


def main():
    global root, table

    root = tk.Tk()
    root.title("Apps List")
    root.geometry("600x400")

    title = tk.Label(root, text="List of Apps", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    columns = ("app_id", "name", "platform")
    table = ttk.Treeview(frame, columns=columns, show="headings")

    table.heading("app_id", text="App ID")
    table.heading("name", text="Name")
    table.heading("platform", text="Platform")

    table.column("app_id", width=100)
    table.column("name", width=250)
    table.column("platform", width=150)

    # Insert data
    for app in apps:
        table.insert("", tk.END, values=(app["id"], app["name"], app["downloads"]))

    # Bind click
    table.bind("<ButtonRelease-1>", on_row_click)

    table.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
