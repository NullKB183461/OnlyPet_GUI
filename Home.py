# home.py
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# -------------------------
# Helper / Setup
# -------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

WINDOW_W, WINDOW_H = 1440, 1024

# Colors
BG_MAIN = "#FFFBEA"
HEADER_TEXT = "#987F50"
HOME_ACTIVE = "#B38633"
OTHER_NAV = "#987F50"
LINE_COLOR = "#AEAEAC"
HOUSE_BG = "#DAB26A"
BTN_BG = "#B99E6C"
BTN_BG_ACTIVE = "#A79779"
CARD_BG = "#9B2A2A"
TEXT_DARK = "#383632"
LOGO_BG = "#FFFFFF"

# Get user full name
user_fullname = sys.argv[1] if len(sys.argv) > 1 else "Guest User"

# -------------------------
# Root window
# -------------------------
root = ctk.CTk()
root.geometry(f"{WINDOW_W}x{WINDOW_H}")
root.resizable(True, True)
root.title("Home - ONLYPETS")

# Main background frame
main_frame = ctk.CTkFrame(root, fg_color=BG_MAIN, corner_radius=0)
main_frame.pack(fill="both", expand=True)

# -------------------------
# Header
# -------------------------
header_frame = tk.Frame(main_frame, bg=BG_MAIN, height=96)
header_frame.pack(fill="x", pady=(16, 8))

# Left side: Logo + Title
logo_canvas = tk.Canvas(header_frame, width=48, height=48, highlightthickness=0, bg=BG_MAIN)
logo_canvas.pack(side="left", padx=(47, 12))
logo_canvas.create_oval(0, 0, 48, 48, fill=LOGO_BG, outline="#E0D6B4")
logo_canvas.create_text(24, 24, text="OP", font=("Poppins Bold", 12), fill=HEADER_TEXT)

title_label = tk.Label(header_frame, text="ONLYPETS", font=("Poppins Bold", 32), fg=HEADER_TEXT, bg=BG_MAIN)
title_label.pack(side="left")

# Center navigation
nav_frame = tk.Frame(header_frame, bg=BG_MAIN)
nav_frame.pack(side="left", expand=True)

nav_items = ["Home", "Adoption", "Service", "Products", "Contact"]
nav_labels = {}

def nav_click(name):
    messagebox.showinfo("Navigation", f"You clicked: {name}")

for item in nav_items:
    fg = HOME_ACTIVE if item == "Home" else OTHER_NAV
    lbl = tk.Label(nav_frame, text=item, font=("Poppins Medium", 20), fg=fg, bg=BG_MAIN, cursor="hand2")
    lbl.pack(side="left", padx=18)
    lbl.bind("<Button-1>", lambda e, n=item: nav_click(n))
    nav_labels[item] = lbl

# Right side: Notifications + Profile
right_frame = tk.Frame(header_frame, bg=BG_MAIN)
right_frame.pack(side="right", padx=30)

notif_label = tk.Label(right_frame, text="🔔", font=("Arial", 20), bg=BG_MAIN)
notif_label.pack(side="left", padx=10)

profile_canvas = tk.Canvas(right_frame, width=40, height=40, highlightthickness=0, bg=BG_MAIN)
profile_canvas.pack(side="left", padx=10)
profile_canvas.create_oval(0, 0, 40, 40, fill="#F7F2E5", outline="#E0D6B4")
profile_canvas.create_text(20, 20, text="U", font=("Poppins Medium", 12), fill=HEADER_TEXT)

profile_name = tk.Label(right_frame, text=user_fullname, font=("Poppins Medium", 16), fg=HEADER_TEXT, bg=BG_MAIN)
profile_name.pack(side="left", padx=10)

# Divider line
tk.Frame(main_frame, bg=LINE_COLOR, height=1).pack(fill="x", padx=30, pady=(0, 24))

# -------------------------
# Welcome + House side by side
# -------------------------
welcome_house_frame = tk.Frame(main_frame, bg=BG_MAIN)
welcome_house_frame.pack(fill="x", padx=53, pady=(20, 24))

# Left side: Welcome text
welcome_text_frame = tk.Frame(welcome_house_frame, bg=BG_MAIN)
welcome_text_frame.pack(side="left", anchor="n")

welcome_label = tk.Label(
    welcome_text_frame,
    text=f"Welcome, {user_fullname}",
    font=("Poppins Bold", 32),
    fg=HEADER_TEXT,
    bg=BG_MAIN
)
welcome_label.pack(anchor="w", pady=(0, 8))

sub_text = "Find your new best friend and give them a forever home, while we care for all your pet’s needs."
sub_label = tk.Label(
    welcome_text_frame,
    text=sub_text,
    font=("Poppins Semibold", 20),
    fg=HEADER_TEXT,
    bg=BG_MAIN,
    wraplength=700,
    justify="left"
)
sub_label.pack(anchor="w")

# Right side: House frame
house_frame = tk.Frame(welcome_house_frame, width=390, height=417, bg=HOUSE_BG)
house_frame.pack(side="right", anchor="n", padx=(40, 0))

img_canvas = tk.Canvas(house_frame, width=292, height=195, bg="#F3E9D7", highlightthickness=0)
img_canvas.place(relx=0.5, y=24, anchor="n")
img_canvas.create_text(146, 97, text="Image Here", font=("Poppins Medium", 18), fill=TEXT_DARK)

def contact_us():
    messagebox.showinfo("Contact", "Contact us clicked!")

contact_btn = ctk.CTkButton(
    house_frame, text="Contact Us",
    width=141, height=37,
    corner_radius=20,
    fg_color=BTN_BG, text_color=TEXT_DARK,
    font=("Poppins Medium", 16),
    command=contact_us
)
contact_btn.place(relx=0.5, rely=1.0, anchor="s", y=-20)

# Divider
tk.Frame(main_frame, bg=LINE_COLOR, height=1).pack(fill="x", padx=30, pady=(0, 24))

# -------------------------
# Pet Options
# -------------------------
section_frame = tk.Frame(main_frame, bg=BG_MAIN)
section_frame.pack(fill="x", pady=(20, 10))

title_section = tk.Label(
    section_frame,
    text="AVAILABLE PETS TO ADOPT",
    font=("Poppins Bold", 20),
    fg=HEADER_TEXT,
    bg=BG_MAIN
)
title_section.pack(side="left", padx=53)

# NEW: added "Others"
pet_options = ["Dogs", "Cats", "Birds", "Fish", "Others"]
pet_buttons = {}

# Wrapper for right alignment
options_frame = tk.Frame(section_frame, bg=BG_MAIN)
options_frame.pack(side="right", padx=53)

def on_category_click(name):
    for k, btn in pet_buttons.items():
        btn.configure(fg_color=BTN_BG_ACTIVE if k == name else BTN_BG, text_color=TEXT_DARK)
    print("Category selected:", name)

for pname in pet_options:
    b = ctk.CTkButton(
        options_frame, text=pname,
        width=120, height=37,
        corner_radius=20,
        fg_color=BTN_BG,
        text_color=TEXT_DARK,
        font=("Poppins Medium", 16),
        command=lambda n=pname: on_category_click(n)
    )
    b.pack(side="left", padx=6)
    pet_buttons[pname] = b

on_category_click("Dogs")

# -------------------------
# Pet Cards Scroll Area
# -------------------------
cards_frame = tk.Frame(main_frame, bg=BG_MAIN)
cards_frame.pack(fill="x", padx=53, pady=(10, 20))

cards_canvas = tk.Canvas(cards_frame, height=283, bg=BG_MAIN, highlightthickness=0)
cards_canvas.pack(side="left", fill="x", expand=True)

h_scroll = tk.Scrollbar(cards_frame, orient="horizontal", command=cards_canvas.xview)
h_scroll.pack(side="bottom", fill="x")

cards_canvas.configure(xscrollcommand=h_scroll.set)

cards_inner = tk.Frame(cards_canvas, bg=BG_MAIN)
cards_window = cards_canvas.create_window((0, 0), window=cards_inner, anchor="nw")

def make_pet_card(parent, pet_name="Dog", idx=0):
    card = tk.Frame(parent, width=217, height=207, bg=CARD_BG)
    card.pack_propagate(False)
    img_frame = tk.Frame(card, width=187, height=183, bg="#F3E9D7")
    img_frame.pack(pady=(10, 6))
    lbl = tk.Label(img_frame, text=f"{pet_name} {idx+1}", font=("Poppins Medium", 12), bg="#F3E9D7")
    lbl.place(relx=0.5, rely=0.5, anchor="center")
    name_lbl = tk.Label(card, text=f"{pet_name} {idx+1}", font=("Poppins Medium", 12), bg=CARD_BG, fg="#FFFFFF")
    name_lbl.pack()
    def on_card_click(e, idx=idx):
        messagebox.showinfo("Pet Clicked", f"You clicked {pet_name} {idx+1}")
    card.bind("<Button-1>", on_card_click)
    img_frame.bind("<Button-1>", on_card_click)
    lbl.bind("<Button-1>", on_card_click)
    return card

for i in range(12):
    pet_card = make_pet_card(cards_inner, "Dog", i)
    pet_card.pack(side="left", padx=12, pady=10)

def update_scrollregion(event=None):
    cards_canvas.configure(scrollregion=cards_canvas.bbox("all"))

cards_inner.bind("<Configure>", update_scrollregion)

def on_next():
    cards_canvas.xview_scroll(1, "page")

next_btn = ctk.CTkButton(
    main_frame, text="Next",
    width=141, height=37,
    corner_radius=20,
    fg_color=BTN_BG, text_color=TEXT_DARK,
    font=("Poppins Medium", 16),
    command=on_next
)
next_btn.pack(anchor="e", padx=53, pady=(0, 30))

# -------------------------
# Mainloop
# -------------------------
root.mainloop()
