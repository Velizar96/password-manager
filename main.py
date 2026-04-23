from customtkinter import *
from tkinter import *
from CTkMessagebox import CTkMessagebox
import random
import pyperclip
import json
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------------------- FUNCTIONS THAT RETURNS PATHS OF JSON FILES ------------------------------- #
def get_data_path():
    if getattr(sys, 'frozen', False):
        # .exe
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "data.json")


def get_settings_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "settings.json")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list_one = [random.choice(letters) for char in range(nr_letters)]
    password_list_two = [random.choice(symbols) for char in range(nr_symbols)]
    password_list_three = [random.choice(numbers) for char in range(nr_numbers)]
    password_list = password_list_one + password_list_two + password_list_three

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- FUNCTION FOR SHOWING PASSWORD ------------------------------- #
def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.configure(show="*")
    else:
        password_entry.configure(show="")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        CTkMessagebox(title=website, message="Please fill in all fields before saving.")
        return
    else:
        try:
            with open(get_data_path(), "r") as file:
                # reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open(get_data_path(), "w") as file:
                # saving data
                json.dump(new_data, file, indent=4)
        else:
            # updating old data with new data
            data.update(new_data)
            with open(get_data_path(), "w") as file:
                # saving data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SAVING THEME ------------------------------- #
def save_theme(theme):
    with open(get_settings_path(), "w") as file:
        json.dump({"theme": theme}, file, indent=4)


def load_theme():
    try:
        with open(get_settings_path(), "r") as file:
            data = json.load(file)
            return data.get("theme", "dark")
    except FileNotFoundError:
        return "dark"


# ---------------------------- LOADING THEME ON START ------------------------------- #
def loading_theme():
    theme = load_theme()
    if theme == "dark":
        set_dark_mode()
        switch_var.set("on")
    else:
        set_light_mode()
        switch_var.set("off")


# ---------------------------- SEARCHING FOR DATA ------------------------------- #
def search_data():
    website = website_entry.get()

    if len(website) == 0:
        CTkMessagebox(title=website, message="Please fill in the search field first.")
        return

    try:
        with open(get_data_path(), "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="No Data File Found.")
    else:
        if website in data:
            CTkMessagebox(title=website,
                          message=f"Email: {data[website]["email"]}\nPassword: {data[website]["password"]}")
            pyperclip.copy(data[website]['password'])
            website_entry.delete(0, END)
        elif website not in data:
            CTkMessagebox(title=website, message="No data for that site yet.")


# ---------------------------- MODE SETTINGS ------------------------------- #
def set_dark_mode():
    set_appearance_mode("dark")
    window.configure(fg_color="#0F172A")

    website_entry.configure(fg_color="#1E293B", border_color="#334155", text_color="#F1F5F9")
    email_entry.configure(fg_color="#1E293B", border_color="#334155", text_color="#F1F5F9")
    password_entry.configure(fg_color="#1E293B", border_color="#334155", text_color="#F1F5F9")

    website_label.configure(text_color="#F1F5F9")
    email_label.configure(text_color="#F1F5F9")
    password_label.configure(text_color="#F1F5F9")
    switch.configure(progress_color="#22C55E", text_color="#F1F5F9")

    show_password_button.configure(border_color="#334155", hover_color="#1E293B", text_color="#94A3B8")

    canvas.configure(bg="#0F172A")


def set_light_mode():
    set_appearance_mode("light")
    window.configure(fg_color="#F8FAFC")

    website_entry.configure(fg_color="#FFFFFF", border_color="#E2E8F0", text_color="#0F172A")
    email_entry.configure(fg_color="#FFFFFF", border_color="#E2E8F0", text_color="#0F172A")
    password_entry.configure(fg_color="#FFFFFF", border_color="#E2E8F0", text_color="#0F172A")

    website_label.configure(text_color="#0F172A")
    email_label.configure(text_color="#0F172A")
    password_label.configure(text_color="#0F172A")
    switch.configure(fg_color="#D1D5DB", text_color="#0F172A")

    show_password_button.configure(border_color="#E2E8F0", hover_color="#E2E8F0", text_color="#64748B")

    canvas.configure(bg="#F8FAFC")


# ---------------------------- SWITCH BEHAVIOUR ------------------------------- #
def switch_event():
    switch_mode = switch_var.get()
    if switch_mode == "on":
        set_dark_mode()
        save_theme("dark")
    else:
        set_light_mode()
        save_theme("light")


# ---------------------------- UI SETUP ------------------------------- #
window = CTk()
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.title("Password Manager")
window.configure(padx=50, pady=50, fg_color="#0F172A")
set_appearance_mode("dark")

# Canvas
canvas = Canvas(width=200, height=200, bg="#0F172A", highlightthickness=0)
logo_img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, padx=10, pady=10)

# Labels
website_label = CTkLabel(window, text="Website:")
website_label.grid(column=0, row=1, pady=5, sticky="W")

email_label = CTkLabel(window, text="Email/Username:")
email_label.grid(column=0, row=2, padx=(0, 20), pady=5, sticky="W")

password_label = CTkLabel(window, text="Password:")
password_label.grid(column=0, row=3, pady=5, sticky="W")

# Entries
website_entry = CTkEntry(window, corner_radius=8)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

email_entry = CTkEntry(window, corner_radius=8)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

password_entry = CTkEntry(window, corner_radius=8, show="*")
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
search_button = CTkButton(window, text="Search Password", command=search_data, fg_color="#3B82F6",
                          hover_color="#2563EB", text_color="#FFFFFF", corner_radius=8)
search_button.grid(column=2, row=1, pady=5, padx=5, sticky="EW")

show_password_button = CTkButton(window, text="👁", corner_radius=8, width=10, fg_color="transparent", anchor="n",
                                 border_width=1, command=toggle_password)
show_password_button.grid(column=2, row=3, sticky="W", padx=(1, 2))

generate_button = CTkButton(window, text="Generate", command=generate_password, fg_color="#3B82F6",
                            hover_color="#2563EB", text_color="#FFFFFF", corner_radius=8, width=118)
generate_button.grid(column=2, row=3, padx=(1, 0), pady=(2, 0), sticky="E")

add_button = CTkButton(window, text="Add", command=save_data, fg_color="#22C55E", hover_color="#16A34A",
                       text_color="#FFFFFF", corner_radius=10)
add_button.grid(column=1, row=4, pady=(15, 40), columnspan=2, sticky="EW")

# ---------------------------- SWITCH AND LOADING LAST THEME ------------------------------- #
switch_var = StringVar(value="on")
switch = CTkSwitch(window, text="Switch Night Mode", command=switch_event, variable=switch_var, onvalue="on",
                   offvalue="off", corner_radius=8)
switch.grid(column=2, row=0, sticky="NW")
loading_theme()

window.mainloop()
