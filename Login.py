import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re
import subprocess

# Setup
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Default theme

# Validation Functions
def is_valid_email(email):
    return email.endswith("@gmail.com") and "@" in email and len(email) > 10

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # at least 1 uppercase
        return False
    if not re.search(r"[^A-Za-z0-9]", password):  # at least 1 special char
        return False
    return True

# Main window
root = ctk.CTk()
root.geometry("1440x1024")
root.title("Log in")
root.configure(bg="#B9A67C")

# Right frame (box)
right_frame = ctk.CTkFrame(
    master=root,
    width=720,
    height=1024,
    fg_color="#B9A67C",
    corner_radius=0
)
right_frame.place(x=815, y=0)

# Title Label
title_label = tk.Label(
    right_frame,
    text="WELCOME TO ONLYPETS",
    font=("Poppins Bold", 36),
    fg="#FFD484",
    bg="#B9A67C"
)
title_label.place(x=170, y=190)

# Subtitle Label
subtitle_label = tk.Label(
    right_frame,
    text="Where Every Paw Finds a Home!",
    font=("Poppins Medium", 20),
    fg="#FFFFFF",
    bg="#B9A67C",
    wraplength=700,
    justify="center"
)
subtitle_label.place(x=265, y=254)

# Entry Box Styling
entry_width = 636
entry_height = 68
entry_color = "#FFFBEA"
text_color = "#383632"
entry_font = ("Poppins Medium", 22)

# Email Address
email_entry = ctk.CTkEntry(
    master=right_frame,
    placeholder_text="Email Address",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font
)
email_entry.place(x=42, y=250)

# Password
password_entry = ctk.CTkEntry(
    master=right_frame,
    placeholder_text="Password",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font,
    show="*"
)
password_entry.place(x=42, y=334)

# Frame to hold Remember Me + Forgot Password
options_frame = tk.Frame(right_frame, bg="#B9A67C")
options_frame.place(x=100, y=520)  # just below password

# Remember Me Checkbox
remember_me = ctk.CTkCheckBox(
    master=options_frame,
    text="Remember Me",
    font=("Poppins Medium", 20),
    text_color="#FFFFFF",
    fg_color="#FFFBEA",
    hover_color="#E6D8B5",
    corner_radius=8
)
remember_me.pack(side="left", padx=(0, 20))

# Forgot Password Label (clickable)
def forgot_password_action(event):
    messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")

forgot_password_label = tk.Label(
    options_frame,
    text="Forgot Password?",
    font=("Poppins Medium", 18),
    fg="#FFFFFF",
    bg="#B9A67C",
    cursor="hand2"
)
forgot_password_label.pack(side="left", padx=(260, 0))
forgot_password_label.bind("<Button-1>", forgot_password_action)

# Login Function
def login_action():
    email = email_entry.get()
    password = password_entry.get()

    if not is_valid_email(email):
        messagebox.showerror("Error", "Email must be a valid Gmail address (example@gmail.com).")
        return

    if not is_valid_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters, include 1 uppercase and 1 special character.")
        return

    # If valid → go to Home.py
    root.withdraw()
    subprocess.Popen(["python", "Home.py"])

# Login Button
login_btn = ctk.CTkButton(
    master=right_frame,
    text="Sign In",
    width=233,
    height=68,
    corner_radius=40,
    fg_color="#F0E4B1",
    hover_color="#e0d3a0",
    text_color="#383632",
    font=("Poppins Medium", 22),
    command=login_action
)
login_btn.place(x=240, y=455)

# "Already have an account?" and "Sign Up Now"
account_frame = tk.Frame(right_frame, width=374, height=30, bg="#B9A67C")
account_frame.place(x=215, y=670)

account_label = tk.Label(
    account_frame,
    text="Don’t have an Account?",
    font=("Poppins", 20),
    fg="#FFFFFF",
    bg="#B9A67C"
)
account_label.pack(side="left")

def open_signup(event=None):
    root.destroy()
    subprocess.Popen(["python", "Signup.py"])

login_label = tk.Label(
    account_frame,
    text=" Sign Up Now",
    font=("Poppins Semibold", 20),
    fg="#FFD484",
    bg="#B9A67C",
    cursor="hand2"
)
login_label.pack(side="left")
login_label.bind("<Button-1>", open_signup)

root.mainloop()
