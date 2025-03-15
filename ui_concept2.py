from customtkinter import *
from tkinter import BOTH, Text
from lib.CTkMenuBar import *
from datetime import datetime
import json
import re
import requests
from xml.etree import ElementTree
from PIL import Image

# Version and player data
version = "1.0.0"
file = None
players = [
    {'id': '76561199230772243', 'name': 'NoedL', 'health': 130},
    {'id': '76561199025920273', 'name': 'Spongebob', 'health': 110}
]

# Initialize window
root = CTk()
root.geometry("690x440")
root.title("R.E.P.O Save Editor")
root.iconbitmap("icon.ico")
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

# ========== World Tab ==========
frame_world = CTkFrame(tabview.tab("World"))
frame_world.pack(fill=BOTH, expand=True, padx=10, pady=10)

def create_entry(label, parent, color):
    frame = CTkFrame(parent, fg_color=color)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=label, font=font).pack(side="left", padx=5)
    entry = CTkEntry(frame, font=font, width=100)
    entry.pack(side="right", padx=5)
    return entry

entry_currency = create_entry("Currency:", frame_world, "#292929")
entry_lives = create_entry("Lives:", frame_world, "#292929")
entry_charging = create_entry("Charging Station Charge's:", frame_world, "#292929")
entry_haul = create_entry("Total Haul:", frame_world, "#292929")

frame_items = CTkFrame(frame_world, corner_radius=10)
frame_items.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_items, text="Items", font=font).pack(anchor="w", padx=10, pady=5)
CTkLabel(frame_items, text="Coming Soon", font=font, text_color="white").pack(fill=BOTH, expand=True)

# ========== Player Tab ==========
frame_player = CTkFrame(tabview.tab("Player"))
frame_player.pack(fill=BOTH, expand=True, padx=10, pady=10)

player_entries = {}

for player in players:
    frame = CTkFrame(frame_player, corner_radius=6)
    frame.pack(fill="x", pady=3)
    # Create Profile picture of the player
    # Fetch profile picture from Steam using player ID
    def fetch_steam_profile_picture(player_id):
        url = f"https://steamcommunity.com/profiles/{player_id}/?xml=1"
        response = requests.get(url)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            avatar_icon = tree.find('avatarIcon')
            if avatar_icon is not None:
                return avatar_icon.text
        # return "profile.png"  # Default profile picture

    profile_picture_url = fetch_steam_profile_picture(player['id'])
    if profile_picture_url:
        image = Image.open(requests.get(profile_picture_url, stream=True).raw)
    else:
        image = Image.open("example.png")

    my_image = CTkImage(light_image=image, dark_image=image, size=(30, 30))
    image_label = CTkLabel(frame, image=my_image, text="")
    image_label.pack(side="left", padx=(10, 5))

    CTkLabel(frame, text=player['name'], font=font).pack(anchor="w", padx=5, pady=3)

    health_entry = create_entry("Health:", frame, "#292929")
    health_entry.insert(0, player['health'])
    
    player_entries[player['name']] = health_entry

# ========== Advanced Tab (JSON Editor with Syntax Highlighting) ==========
def highlight_json():
    """ Highlights JSON syntax in the text widget. """
    textbox.tag_remove("key", "1.0", "end")
    textbox.tag_remove("string", "1.0", "end")
    textbox.tag_remove("number", "1.0", "end")
    textbox.tag_remove("boolean", "1.0", "end")

    json_text = textbox.get("1.0", "end-1c")

    key_pattern = r'(\"[^\"]*\")\s*:'
    string_pattern = r'(:\s*)("(?:\\.|[^"\\])*")'
    number_pattern = r'(:\s*)(\d+(\.\d+)?)'
    boolean_pattern = r'(:\s*)(true|false|null)'

    for match in re.finditer(key_pattern, json_text):
        start, end = f"1.0+{match.start()}c", f"1.0+{match.end(1)}c"
        textbox.tag_add("key", start, end)

    for match in re.finditer(string_pattern, json_text):
        start, end = f"1.0+{match.start(2)}c", f"1.0+{match.end(2)}c"
        textbox.tag_add("string", start, end)

    for match in re.finditer(number_pattern, json_text):
        start, end = f"1.0+{match.start(2)}c", f"1.0+{match.end(2)}c"
        textbox.tag_add("number", start, end)

    for match in re.finditer(boolean_pattern, json_text):
        start, end = f"1.0+{match.start(2)}c", f"1.0+{match.end(2)}c"
        textbox.tag_add("boolean", start, end)

def update_json(event):
    """ Updates JSON and applies highlighting """
    try:
        data = json.loads(textbox.get("1.0", "end-1c"))
        print("JSON updated:", data)
        highlight_json()
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)

frame_advanced = CTkFrame(tabview.tab("Advanced"))
frame_advanced.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_advanced, text="Edit JSON:", font=font).pack(anchor="w", padx=5, pady=3)

textbox = Text(frame_advanced, font=("Courier", 10), height=12, wrap="word", bg="#2b2b2b", fg="white", insertbackground="white")
textbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
textbox.bind("<KeyRelease>", update_json)
textbox.insert("1.0", json.dumps(players, indent=4))

textbox.tag_configure("key", foreground="#FFCC00")      # Yellow for keys
textbox.tag_configure("string", foreground="#99CC99")   # Green for strings
textbox.tag_configure("number", foreground="#FF6666")   # Red for numbers
textbox.tag_configure("boolean", foreground="#66CCFF")  # Blue for booleans

highlight_json()

# ========== Footer ==========
label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
label_footer.pack(side="bottom", pady=5)

root.mainloop()
