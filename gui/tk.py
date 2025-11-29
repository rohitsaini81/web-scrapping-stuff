import tkinter as tk
from tkinter import messagebox

def say_hello():
    messagebox.showinfo("Hello", "Welcome to Tkinter GUI!")

root = tk.Tk()
root.title("Tkinter Example")
root.geometry("300x150")

label = tk.Label(root, text="Hello Tkinter!")
label.pack(pady=10)

button = tk.Button(root, text="Click Me", command=say_hello)
button.pack(pady=10)

root.mainloop()

