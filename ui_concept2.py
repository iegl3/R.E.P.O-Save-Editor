from customtkinter import *
from tkinter import BOTH
from lib.CTkMenuBar import *
from datetime import datetime
import json

version = "1.0.0"
file = None
players = [
    {'name': 'NoedL', 'health': 130},
    {'name': 'Spongebob', 'health': 110}
]

root = CTk()
root.geometry("690x440")
root.title("R.E.P.O Save Editor")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Font settings
font = ("Arial", 12)
small_font = ("Arial", 9)

# Menu
menu = CTkTitleMenu(master=root)
button_file = menu.add_cascade("File")
dropdown1 = CustomDropdownMenu(widget=button_file)
dropdown1.add_option(option="Open", command=lambda: print("Open"))
dropdown1.add_option(option="Save", command=lambda: print("Save"))
dropdown1.add_separator()
sub_menu = dropdown1.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".JSON")

# Tabview
tabview = CTkTabview(root, width=680, height=400)
tabview.pack(fill=BOTH, expand=True)
tabview.add("World")
tabview.add("Player")
tabview.add("Advanced")

# World Tab
frame_world = CTkFrame(tabview.tab("World"))
frame_world.pack(fill=BOTH, expand=True, padx=10, pady=10)

def create_entry(label, parent):
    frame = CTkFrame(parent)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=label, font=font).pack(side="left", padx=5)
    entry = CTkEntry(frame, font=font, width=100)
    entry.pack(side="right", padx=5)
    return entry

entry_balance = create_entry("Balance:", frame_world)
entry_currency = create_entry("Currency:", frame_world)
entry_lives = create_entry("Lives:", frame_world)
entry_charging = create_entry("Charging Station Charge's:", frame_world)
entry_haul = create_entry("Total Haul:", frame_world)

frame_items = CTkFrame(frame_world, corner_radius=10)
frame_items.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_items, text="Items", font=font).pack(anchor="w", padx=10, pady=5)
CTkLabel(frame_items, text="Coming Soon", font=font, text_color="white").pack(fill=BOTH, expand=True)

# Player Tab
frame_player = CTkFrame(tabview.tab("Player"))
frame_player.pack(fill=BOTH, expand=True, padx=10, pady=10)
for player in players:
    frame = CTkFrame(frame_player, corner_radius=6)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=player['name'], font=font).pack(anchor="w", padx=5, pady=3)
    health_entry = create_entry("Health:", frame)
    health_entry.insert(0, player['health'])

# Advanced Tab
def update_json(event):
    try:
        data = json.loads(textbox.get("1.0", "end-1c"))
        print("JSON updated:", data)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)

frame_advanced = CTkFrame(tabview.tab("Advanced"))
frame_advanced.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_advanced, text="Edit JSON:", font=font).pack(anchor="w", padx=5, pady=3)
textbox = CTkTextbox(frame_advanced, font=("Courier", 10), height=200)
textbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
textbox.bind("<KeyRelease>", update_json)
textbox.insert("1.0", json.dumps(players, indent=4))

# Footer
label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
label_footer.pack(side="bottom", pady=5)

root.mainloop()