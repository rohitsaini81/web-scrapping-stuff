import tkinter as tk
from tkinter import messagebox

def submit_form():
    data = f"""
Name: {entry_name.get()}
Email: {entry_email.get()}
Password: {entry_password.get()}
Gender: {gender_var.get()}
Subscribe: {'Yes' if subscribe_var.get() else 'No'}
Country: {country_var.get()}
Comments: {text_comments.get("1.0", tk.END).strip()}
"""
    messagebox.showinfo("Form Submitted", data)

def reset_form():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    gender_var.set("Male")
    subscribe_var.set(0)
    country_var.set(countries[0])
    text_comments.delete("1.0", tk.END)

root = tk.Tk()
root.title("Tkinter Form Example")
root.geometry("400x500")
root.resizable(False, False)

# --- Form Fields ---
tk.Label(root, text="Name").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Password").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_password = tk.Entry(root, show="*", width=30)
entry_password.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Gender").grid(row=3, column=0, sticky="w", padx=10, pady=5)
gender_var = tk.StringVar(value="Male")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=3, column=1, sticky="e")

subscribe_var = tk.IntVar()
tk.Checkbutton(root, text="Subscribe to newsletter", variable=subscribe_var).grid(row=4, columnspan=2, padx=10, pady=5)

tk.Label(root, text="Country").grid(row=5, column=0, sticky="w", padx=10, pady=5)
countries = ["Select", "USA", "India", "UK", "Canada"]
country_var = tk.StringVar(value=countries[0])
tk.OptionMenu(root, country_var, *countries).grid(row=5, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Comments").grid(row=6, column=0, sticky="nw", padx=10, pady=5)
text_comments = tk.Text(root, width=30, height=5)
text_comments.grid(row=6, column=1, padx=10, pady=5)

# --- Buttons ---
tk.Button(root, text="Submit", command=submit_form, width=12).grid(row=7, column=0, padx=10, pady=20)
tk.Button(root, text="Reset", command=reset_form, width=12).grid(row=7, column=1, padx=10, pady=20)

root.mainloop()

