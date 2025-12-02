import tkinter as tk

class Navbar(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="#1f1f1f", height=50)
        self.root = root

        self.pack(fill="x")

        # ---- Buttons ----
        tk.Button(self, text="Apps", fg="white", bg="#333",
                  command=lambda: root.show_apps_screen()).pack(side="left", padx=10)

        tk.Button(self, text="Preview", fg="white", bg="#333",
                  command=lambda: root.go_preview_if_exists()).pack(side="left", padx=10)

        tk.Button(self, text="Settings", fg="white", bg="#333",
                  command=lambda: root.show_settings_screen()).pack(side="left", padx=10)
