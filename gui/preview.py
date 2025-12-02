import tkinter as tk
from navbar import Navbar
import requests
from PIL import Image, ImageTk
import io


class AppPreview:
    def __init__(self, parent, app_id, name, short_description):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Preview - {name}")
        self.window.geometry("350x250")
        self.window.resizable(False, False)

        tk.Label(self.window, text="App Preview", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.window, text=f"App ID: {app_id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.window, text=f"Name: {name}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.window, text=f"Platform: {short_description}", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=15)







class PreviewScreen(tk.Frame):
    def __init__(self, root, app_id, name, short_description):
        super().__init__(root)
        self.root = root
        self.images = []  # Keep references to images

        # ---------------------------
        # Vertical scroll setup
        # ---------------------------
        v_scroll_frame = tk.Frame(self)
        v_scroll_frame.pack(fill="both", expand=True)

        v_scrollbar = tk.Scrollbar(v_scroll_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(v_scroll_frame, yscrollcommand=v_scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.config(command=canvas.yview)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Update scroll region dynamically
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", update_scroll_region)

        # ---------------------------
        # Fetch App Data
        # ---------------------------
        responseApp = requests.get(f"http://localhost:5000/api/app/{app_id}")
        app_data = responseApp.json()
        description = app_data.get("description", short_description)

        app_table_id = app_data["id"]
        responseSS = requests.get(f"http://localhost:5000/api/app/screenshots/{app_table_id}")
        app_screenshots = responseSS.json()

        # ---------------------------
        # Header
        # ---------------------------
        tk.Label(inner_frame, text="App Preview", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(inner_frame, text=f"App ID: {app_id}", font=("Arial", 14)).pack(pady=2)
        tk.Label(inner_frame, text=f"Name: {name}", font=("Arial", 14)).pack(pady=2)

        # ---------------------------
        # Description
        # ---------------------------
        text = tk.Text(inner_frame, wrap="word", font=("Arial", 14), height=10)
        text.insert("1.0", description)
        text.config(state="disabled")
        text.pack(fill="both", expand=False, padx=10, pady=5)

        # ---------------------------
        # Scrollable Screenshots (horizontal)
        # ---------------------------
        canvas_frame = tk.Frame(inner_frame)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        h_canvas = tk.Canvas(canvas_frame, height=400)
        h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=h_canvas.xview)
        h_canvas.configure(xscrollcommand=h_scroll.set)

        h_scroll.pack(side="bottom", fill="x")
        h_canvas.pack(side="left", fill="both", expand=True)

        container = tk.Frame(h_canvas)
        h_canvas.create_window((0, 0), window=container, anchor="nw")

        container.bind("<Configure>", lambda e: h_canvas.configure(scrollregion=h_canvas.bbox("all")))

        for screenshot in app_screenshots:
            url = screenshot.get("url")
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(io.BytesIO(response.content))
            except Exception as e:
                print("Failed loading image:", url, e)
                img = Image.open("error.png")  # fallback

            img = img.resize((200, 400))
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)

            label = tk.Label(container, image=tk_img)
            label.pack(side="left", padx=5)

        # ---------------------------
        # Back Button
        # ---------------------------
        tk.Button(inner_frame, text="Back", command=root.show_apps_screen).pack(pady=10)
