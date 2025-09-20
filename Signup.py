import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re
import subprocess

# Setup
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Default theme

# Validation Functions
def is_valid_fullname(name):
    return name.replace(" ", "").isalpha()  # only letters and spaces

def is_valid_email(email):
    return email.endswith("@gmail.com") and "@" in email and len(email) > 10

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10  # only digits and at least 10

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
root.title("Sign Up")
root.configure(bg="#B9A67C")

# Left frame (box)
left_frame = ctk.CTkFrame(
    master=root,
    width=720,
    height=1024,
    fg_color="#B9A67C",
    corner_radius=0
)
left_frame.place(x=0, y=0)

# Title Label
title_label = tk.Label(
    left_frame,
    text="CREATE ACCOUNT",
    font=("Poppins Bold", 36),
    fg="#FFD484",
    bg="#B9A67C"
)
title_label.place(x=220, y=190)

# Subtitle Label
subtitle_label = tk.Label(
    left_frame,
    text="Start your journey with us — pets are waiting for you!",
    font=("Poppins Medium", 20),
    fg="#FFFFFF",
    bg="#B9A67C",
    wraplength=700,
    justify="center"
)
subtitle_label.place(x=125, y=254)

# Entry Box Styling
entry_width = 636
entry_height = 68
entry_color = "#FFFBEA"
text_color = "#383632"
entry_font = ("Poppins Medium", 22)

# Full Name (letters only)
fullname_entry = ctk.CTkEntry(
    master=left_frame,
    placeholder_text="Full Name",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font
)
fullname_entry.place(x=42, y=250)

def allow_letters(event=None):
    value = fullname_entry.get()
    filtered = "".join(ch for ch in value if ch.isalpha() or ch.isspace())
    if value != filtered:
        fullname_entry.delete(0, "end")
        fullname_entry.insert(0, filtered)

fullname_entry.bind("<KeyRelease>", allow_letters)
fullname_entry.bind("<<Paste>>", allow_letters)

# Email Address
email_entry = ctk.CTkEntry(
    master=left_frame,
    placeholder_text="Email Address",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font
)
email_entry.place(x=42, y=334)

# Phone Number (digits only)
phone_entry = ctk.CTkEntry(
    master=left_frame,
    placeholder_text="Phone Number",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font
)
phone_entry.place(x=42, y=418)

def allow_digits(event=None):
    value = phone_entry.get()
    filtered = "".join(ch for ch in value if ch.isdigit())
    if value != filtered:
        phone_entry.delete(0, "end")
        phone_entry.insert(0, filtered)

phone_entry.bind("<KeyRelease>", allow_digits)
phone_entry.bind("<<Paste>>", allow_digits)

# Password
password_entry = ctk.CTkEntry(
    master=left_frame,
    placeholder_text="Password",
    width=entry_width,
    height=entry_height,
    corner_radius=40,
    fg_color=entry_color,
    text_color=text_color,
    font=entry_font,
    show="*"
)
password_entry.place(x=42, y=502)

# Sign Up Button
def signup_action():
    fullname = fullname_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()

    if not fullname or not email or not phone or not password:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    if not is_valid_fullname(fullname):
        messagebox.showerror("Error", "Full Name must only contain letters and spaces.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Email must be a valid Gmail address (example@gmail.com).")
        return

    if not is_valid_phone(phone):
        messagebox.showerror("Error", "Phone Number must contain only digits and be at least 10 numbers.")
        return

    if not is_valid_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters, include 1 uppercase and 1 special character.")
        return

    messagebox.showinfo("Success", "Account created successfully!")

    # Redirect to Login.py
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

signup_btn = ctk.CTkButton(
    master=left_frame,
    text="Sign Up",
    width=233,
    height=68,
    corner_radius=40,
    fg_color="#F0E4B1",
    hover_color="#e0d3a0",
    text_color="#383632",
    font=("Poppins Medium", 22),
    command=signup_action
)
signup_btn.place(x=227, y=590)

# "Already have an account?" and "Login Now"
account_frame = tk.Frame(left_frame, width=374, height=30, bg="#B9A67C")
account_frame.place(x=190, y=840)

account_label = tk.Label(
    account_frame,
    text="Already have an Account?",
    font=("Poppins", 20),
    fg="#FFFFFF",
    bg="#B9A67C"
)
account_label.pack(side="left")

login_label = tk.Label(
    account_frame,
    text=" Login Now",
    font=("Poppins Semibold", 20),
    fg="#FFD484",
    bg="#B9A67C",
    cursor="hand2"
)
login_label.pack(side="left")

def login_action(event=None):
    root.destroy()
    subprocess.Popen(["python", "Login.py"])

login_label.bind("<Button-1>", login_action)

root.mainloop()
