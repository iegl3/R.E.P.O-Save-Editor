from customtkinter import *
from tkinter import BOTH, Text
from lib.CTkMenuBar import *
from datetime import datetime
import json
import re
import requests
from xml.etree import ElementTree
from PIL import Image
from tkinter import filedialog
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "noedl.xyz"  # This creates a .cache folder inside the user's home directory
CACHE_DIR.mkdir(parents=True, exist_ok=True)

print(CACHE_DIR)

# Version and player data
version = "1.0.0"
file = None
players = [
]

json_data = {
    "dictionaryOfDictionaries": {
        "__type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089],[System.Collections.Generic.Dictionary`2[[System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089],[System.Int32, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089]], mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089]],mscorlib",
        "value": {
            "runStats": {
                "level": 3,
                "currency": 130,
                "lives": 3,
                "chargingStationCharge": 4,
                "totalHaul": 35,
                "save level": 0
            },
            "itemsPurchased": {
                "Item Cart Medium": 4,
                "Item Cart Small": 2,
                "Item Drone Battery": 0,
                "Item Drone Feather": 1,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 1,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 1,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 0,
                "Item Grenade Stun": 0,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 1,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 2,
                "Item Health Pack Medium": 2,
                "Item Health Pack Small": 3,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 1,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 1,
                "Item Melee Sword": 1,
                "Item Mine Explosive": 1,
                "Item Mine Shockwave": 0,
                "Item Mine Stun": 0,
                "Item Orb Zero Gravity": 1,
                "Item Power Crystal": 4,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 0,
                "Item Upgrade Player Energy": 0,
                "Item Upgrade Player Extra Jump": 0,
                "Item Upgrade Player Grab Range": 0,
                "Item Upgrade Player Grab Strength": 0,
                "Item Upgrade Player Health": 0,
                "Item Upgrade Player Sprint Speed": 0,
                "Item Upgrade Player Tumble Launch": 0,
                "Item Valuable Tracker": 1
            },
            "itemsPurchasedTotal": {
                "Item Cart Medium": 4,
                "Item Cart Small": 2,
                "Item Drone Battery": 0,
                "Item Drone Feather": 1,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 1,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 3,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 2,
                "Item Grenade Stun": 1,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 1,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 3,
                "Item Health Pack Medium": 3,
                "Item Health Pack Small": 3,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 1,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 1,
                "Item Melee Sword": 1,
                "Item Mine Explosive": 1,
                "Item Mine Shockwave": 1,
                "Item Mine Stun": 1,
                "Item Orb Zero Gravity": 1,
                "Item Power Crystal": 6,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 1,
                "Item Upgrade Player Energy": 7,
                "Item Upgrade Player Extra Jump": 1,
                "Item Upgrade Player Grab Range": 7,
                "Item Upgrade Player Grab Strength": 1,
                "Item Upgrade Player Health": 5,
                "Item Upgrade Player Sprint Speed": 5,
                "Item Upgrade Player Tumble Launch": 2,
                "Item Valuable Tracker": 1
            },
            "itemsUpgradesPurchased": {
                "Item Cart Medium": 0,
                "Item Cart Small": 0,
                "Item Drone Battery": 0,
                "Item Drone Feather": 0,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 0,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 0,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 0,
                "Item Grenade Stun": 0,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 0,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 0,
                "Item Health Pack Medium": 0,
                "Item Health Pack Small": 0,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 0,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 0,
                "Item Melee Sword": 0,
                "Item Mine Explosive": 0,
                "Item Mine Shockwave": 0,
                "Item Mine Stun": 0,
                "Item Orb Zero Gravity": 0,
                "Item Power Crystal": 0,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 1,
                "Item Upgrade Player Energy": 7,
                "Item Upgrade Player Extra Jump": 1,
                "Item Upgrade Player Grab Range": 7,
                "Item Upgrade Player Grab Strength": 1,
                "Item Upgrade Player Health": 5,
                "Item Upgrade Player Sprint Speed": 5,
                "Item Upgrade Player Tumble Launch": 2,
                "Item Valuable Tracker": 0
            },
            "itemBatteryUpgrades": {
                "Item Cart Medium": 0,
                "Item Cart Small": 0,
                "Item Drone Battery": 0,
                "Item Drone Feather": 0,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 0,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 0,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 0,
                "Item Grenade Stun": 0,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 0,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 0,
                "Item Health Pack Medium": 0,
                "Item Health Pack Small": 0,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 0,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 0,
                "Item Melee Sword": 0,
                "Item Mine Explosive": 0,
                "Item Mine Shockwave": 0,
                "Item Mine Stun": 0,
                "Item Orb Zero Gravity": 0,
                "Item Power Crystal": 0,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 0,
                "Item Upgrade Player Energy": 0,
                "Item Upgrade Player Extra Jump": 0,
                "Item Upgrade Player Grab Range": 0,
                "Item Upgrade Player Grab Strength": 0,
                "Item Upgrade Player Health": 0,
                "Item Upgrade Player Sprint Speed": 0,
                "Item Upgrade Player Tumble Launch": 0,
                "Item Valuable Tracker": 0
            },
            "playerHealth": {
                "76561199230772243": 140,
                "76561199000416602": 120,
                "76561199240339727": 142
            },
            "playerUpgradeHealth": {
                "76561199230772243": 2,
                "76561199000416602": 1,
                "76561199240339727": 2
            },
            "playerUpgradeStamina": {
                "76561199230772243": 4,
                "76561199000416602": 1,
                "76561199240339727": 2
            },
            "playerUpgradeExtraJump": {
                "76561199230772243": 0,
                "76561199000416602": 0,
                "76561199240339727": 1
            },
            "playerUpgradeLaunch": {
                "76561199230772243": 1,
                "76561199000416602": 2,
                "76561199240339727": 1
            },
            "playerUpgradeMapPlayerCount": {
                "76561199230772243": 0,
                "76561199000416602": 0,
                "76561199240339727": 0
            },
            "playerUpgradeSpeed": {
                "76561199230772243": 2,
                "76561199000416602": 5,
                "76561199240339727": 2
            },
            "playerUpgradeStrength": {
                "76561199230772243": 1,
                "76561199000416602": 1,
                "76561199240339727": 1
            },
            "playerUpgradeRange": {
                "76561199230772243": 4,
                "76561199000416602": 1,
                "76561199240339727": 2
            },
            "playerUpgradeThrow": {
                "76561199230772243": 0,
                "76561199000416602": 0,
                "76561199240339727": 0
            },
            "playerHasCrown": {
                "76561199230772243": 0,
                "76561199000416602": 0,
                "76561199240339727": 0
            },
            "item": {
                "Item Cart Medium": 0,
                "Item Cart Small": 0,
                "Item Drone Battery": 0,
                "Item Drone Feather": 0,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 0,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 0,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 0,
                "Item Grenade Stun": 0,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 0,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 0,
                "Item Health Pack Medium": 0,
                "Item Health Pack Small": 0,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 0,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 0,
                "Item Melee Sword": 0,
                "Item Mine Explosive": 0,
                "Item Mine Shockwave": 0,
                "Item Mine Stun": 0,
                "Item Orb Zero Gravity": 0,
                "Item Power Crystal": 0,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 0,
                "Item Upgrade Player Energy": 0,
                "Item Upgrade Player Extra Jump": 0,
                "Item Upgrade Player Grab Range": 0,
                "Item Upgrade Player Grab Strength": 0,
                "Item Upgrade Player Health": 0,
                "Item Upgrade Player Sprint Speed": 0,
                "Item Upgrade Player Tumble Launch": 0,
                "Item Valuable Tracker": 0,
                "Item Cart Medium/1": 0,
                "Item Upgrade Player Health/1": 35,
                "Item Power Crystal/1": 28,
                "Item Health Pack Large/1": 16,
                "Item Upgrade Player Grab Range/1": 33,
                "Item Health Pack Medium/1": 17,
                "Item Upgrade Player Energy/1": 31,
                "Item Melee Frying Pan/1": 20,
                "Item Health Pack Small/1": 18,
                "Item Health Pack Small/2": 18,
                "Item Grenade Human/1": 10,
                "Item Grenade Duct Taped/1": 8,
                "Item Melee Sword/1": 23,
                "Item Power Crystal/2": 28,
                "Item Gun Shotgun/1": 14,
                "Item Upgrade Player Tumble Launch/1": 37,
                "Item Valuable Tracker/1": 38,
                "Item Health Pack Large/3": 16,
                "Item Upgrade Player Grab Range/2": 33,
                "Item Power Crystal/3": 28,
                "Item Cart Small/1": 1,
                "Item Upgrade Map Player Count/1": 30,
                "Item Melee Inflatable Hammer/1": 21,
                "Item Upgrade Player Grab Range/3": 33,
                "Item Upgrade Player Sprint Speed/1": 36,
                "Item Upgrade Player Grab Strength/1": 34,
                "Item Upgrade Player Extra Jump/1": 32,
                "Item Melee Frying Pan/2": 20,
                "Item Melee Sledge Hammer/1": 22,
                "Item Mine Shockwave/2": 25,
                "Item Health Pack Small/3": 18,
                "Item Health Pack Large/4": 16,
                "Item Health Pack Large/5": 16,
                "Item Health Pack Small/4": 18,
                "Item Upgrade Player Grab Strength/2": 34,
                "Item Health Pack Large/6": 16,
                "Item Grenade Shockwave/3": 11,
                "Item Cart Small/2": 1,
                "Item Health Pack Medium/2": 17,
                "Item Upgrade Player Energy/2": 31,
                "Item Valuable Tracker/2": 38,
                "Item Upgrade Player Extra Jump/2": 32,
                "Item Upgrade Player Health/2": 35,
                "Item Upgrade Player Tumble Launch/2": 37,
                "Item Upgrade Player Grab Range/4": 33,
                "Item Upgrade Map Player Count/2": 30,
                "Item Upgrade Player Grab Range/5": 33,
                "Item Upgrade Player Grab Range/6": 33,
                "Item Upgrade Player Sprint Speed/2": 36,
                "Item Grenade Shockwave/4": 11,
                "Item Drone Feather/1": 3,
                "Item Extraction Tracker/1": 7,
                "Item Mine Explosive/1": 24,
                "Item Melee Sword/2": 23,
                "Item Drone Feather/2": 3,
                "Item Orb Zero Gravity/1": 27,
                "Item Grenade Explosive/3": 9,
                "Item Upgrade Player Grab Range/7": 33,
                "Item Upgrade Player Health/3": 35,
                "Item Upgrade Player Grab Range/8": 33,
                "Item Upgrade Player Grab Range/9": 33,
                "Item Upgrade Player Sprint Speed/3": 36,
                "Item Upgrade Player Sprint Speed/4": 36,
                "Item Extraction Tracker/2": 7,
                "Item Cart Small/3": 1,
                "Item Upgrade Player Energy/3": 31,
                "Item Upgrade Player Health/4": 35,
                "Item Mine Stun/2": 26,
                "Item Mine Explosive/2": 24,
                "Item Health Pack Medium/4": 17,
                "Item Upgrade Player Energy/4": 31,
                "Item Cart Medium/2": 0,
                "Item Grenade Explosive/4": 9,
                "Item Gun Shotgun/2": 14,
                "Item Grenade Stun/2": 12,
                "Item Orb Zero Gravity/2": 27,
                "Item Upgrade Player Health/5": 35,
                "Item Health Pack Small/5": 18,
                "Item Upgrade Player Energy/5": 31,
                "Item Upgrade Player Energy/6": 31,
                "Item Upgrade Player Sprint Speed/5": 36,
                "Item Upgrade Player Health/6": 35,
                "Item Upgrade Player Sprint Speed/6": 36,
                "Item Upgrade Player Energy/7": 31,
                "Item Upgrade Player Grab Range/10": 33,
                "Item Upgrade Player Tumble Launch/3": 37,
                "Item Upgrade Player Energy/8": 31,
                "Item Cart Medium/3": 0,
                "Item Cart Medium/4": 0,
                "Item Melee Sledge Hammer/2": 22
            },
            "itemStatBattery": {
                "Item Cart Medium": 0,
                "Item Cart Small": 0,
                "Item Drone Battery": 0,
                "Item Drone Feather": 0,
                "Item Drone Indestructible": 0,
                "Item Drone Torque": 0,
                "Item Drone Zero Gravity": 0,
                "Item Extraction Tracker": 0,
                "Item Grenade Duct Taped": 0,
                "Item Grenade Explosive": 0,
                "Item Grenade Human": 0,
                "Item Grenade Shockwave": 0,
                "Item Grenade Stun": 0,
                "Item Gun Handgun": 0,
                "Item Gun Shotgun": 0,
                "Item Gun Tranq": 0,
                "Item Health Pack Large": 0,
                "Item Health Pack Medium": 0,
                "Item Health Pack Small": 0,
                "Item Melee Baseball Bat": 0,
                "Item Melee Frying Pan": 0,
                "Item Melee Inflatable Hammer": 0,
                "Item Melee Sledge Hammer": 0,
                "Item Melee Sword": 0,
                "Item Mine Explosive": 0,
                "Item Mine Shockwave": 0,
                "Item Mine Stun": 0,
                "Item Orb Zero Gravity": 0,
                "Item Power Crystal": 0,
                "Item Rubber Duck": 0,
                "Item Upgrade Map Player Count": 0,
                "Item Upgrade Player Energy": 0,
                "Item Upgrade Player Extra Jump": 0,
                "Item Upgrade Player Grab Range": 0,
                "Item Upgrade Player Grab Strength": 0,
                "Item Upgrade Player Health": 0,
                "Item Upgrade Player Sprint Speed": 0,
                "Item Upgrade Player Tumble Launch": 0,
                "Item Valuable Tracker": 0,
                "Item Cart Medium/1": 100,
                "Item Upgrade Player Health/1": 100,
                "Item Power Crystal/1": 100,
                "Item Health Pack Large/1": 100,
                "Item Upgrade Player Grab Range/1": 100,
                "Item Health Pack Medium/1": 100,
                "Item Upgrade Player Energy/1": 100,
                "Item Melee Frying Pan/1": 99,
                "Item Health Pack Small/1": 100,
                "Item Health Pack Small/2": 100,
                "Item Grenade Human/1": 100,
                "Item Grenade Duct Taped/1": 100,
                "Item Melee Sword/1": 99,
                "Item Power Crystal/2": 100,
                "Item Gun Shotgun/1": 99,
                "Item Upgrade Player Tumble Launch/1": 100,
                "Item Valuable Tracker/1": 99,
                "Item Health Pack Large/3": 100,
                "Item Upgrade Player Grab Range/2": 100,
                "Item Power Crystal/3": 100,
                "Item Cart Small/1": 100,
                "Item Upgrade Map Player Count/1": 100,
                "Item Melee Inflatable Hammer/1": 99,
                "Item Upgrade Player Grab Range/3": 100,
                "Item Upgrade Player Sprint Speed/1": 100,
                "Item Upgrade Player Grab Strength/1": 100,
                "Item Upgrade Player Extra Jump/1": 100,
                "Item Melee Frying Pan/2": 100,
                "Item Melee Sledge Hammer/1": 83,
                "Item Mine Shockwave/2": 100,
                "Item Health Pack Small/3": 100,
                "Item Health Pack Large/4": 100,
                "Item Health Pack Large/5": 100,
                "Item Health Pack Small/4": 100,
                "Item Upgrade Player Grab Strength/2": 100,
                "Item Health Pack Large/6": 100,
                "Item Grenade Shockwave/3": 100,
                "Item Cart Small/2": 100,
                "Item Health Pack Medium/2": 100,
                "Item Upgrade Player Energy/2": 100,
                "Item Valuable Tracker/2": 100,
                "Item Upgrade Player Extra Jump/2": 100,
                "Item Upgrade Player Health/2": 100,
                "Item Upgrade Player Tumble Launch/2": 100,
                "Item Upgrade Player Grab Range/4": 100,
                "Item Upgrade Map Player Count/2": 100,
                "Item Upgrade Player Grab Range/5": 100,
                "Item Upgrade Player Grab Range/6": 100,
                "Item Upgrade Player Sprint Speed/2": 100,
                "Item Grenade Shockwave/4": 100,
                "Item Drone Feather/1": 99,
                "Item Extraction Tracker/1": 83,
                "Item Mine Explosive/1": 100,
                "Item Melee Sword/2": 100,
                "Item Drone Feather/2": 100,
                "Item Orb Zero Gravity/1": 99,
                "Item Grenade Explosive/3": 100,
                "Item Upgrade Player Grab Range/7": 100,
                "Item Upgrade Player Health/3": 100,
                "Item Upgrade Player Grab Range/8": 100,
                "Item Upgrade Player Grab Range/9": 100,
                "Item Upgrade Player Sprint Speed/3": 100,
                "Item Upgrade Player Sprint Speed/4": 100,
                "Item Extraction Tracker/2": 100,
                "Item Cart Small/3": 100,
                "Item Upgrade Player Energy/3": 100,
                "Item Upgrade Player Health/4": 100,
                "Item Mine Stun/2": 100,
                "Item Mine Explosive/2": 100,
                "Item Health Pack Medium/4": 100,
                "Item Upgrade Player Energy/4": 100,
                "Item Cart Medium/2": 100,
                "Item Grenade Explosive/4": 100,
                "Item Gun Shotgun/2": 100,
                "Item Grenade Stun/2": 100,
                "Item Orb Zero Gravity/2": 100,
                "Item Upgrade Player Health/5": 100,
                "Item Health Pack Small/5": 100,
                "Item Upgrade Player Energy/5": 100,
                "Item Upgrade Player Energy/6": 100,
                "Item Upgrade Player Sprint Speed/5": 100,
                "Item Upgrade Player Health/6": 100,
                "Item Upgrade Player Sprint Speed/6": 100,
                "Item Upgrade Player Energy/7": 100,
                "Item Upgrade Player Grab Range/10": 100,
                "Item Upgrade Player Tumble Launch/3": 100,
                "Item Upgrade Player Energy/8": 100,
                "Item Cart Medium/3": 100,
                "Item Cart Medium/4": 100,
                "Item Melee Sledge Hammer/2": 100
            }
        }
    },
    "playerNames": {
        "__type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089],[System.String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089]],mscorlib",
        "value": {
            "76561199230772243": "NoedL",
            "76561199000416602": "Streal",
            "76561199240339727": "Ruben"
        }
    },
    "timePlayed": {
        "__type": "float",
        "value": 1740.98694
    },
    "dateAndTime": {
        "__type": "string",
        "value": "2025-03-15"
    },
    "teamName": {
        "__type": "string",
        "value": "R.E.P.O."
    }
}

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
dropdown1.add_option(option="Open", command=lambda: open_file())
dropdown1.add_option(option="Save", command=lambda: save_data())
dropdown1.add_separator()
sub_menu = dropdown1.add_submenu("Export As (Currently Unavailable)")
# sub_menu.add_option(option=".TXT (Currently Unavailable)")
# sub_menu.add_option(option=".JSON (Currently Unavailable)")

# Tabview
tabview = CTkTabview(root, width=680, height=400)
tabview.pack(fill=BOTH, expand=True)
tabview.add("World")
tabview.add("Player")
tabview.add("Advanced")

# ========== World Tab ========== 
frame_world = CTkFrame(tabview.tab("World"))
frame_world.pack(fill=BOTH, expand=True, padx=10, pady=10)

def create_entry(label, parent, color, update_callback=None):
    frame = CTkFrame(parent, fg_color=color)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=label, font=font).pack(side="left", padx=5)
    entry = CTkEntry(frame, font=font, width=100)
    entry.pack(side="right", padx=5)
    
    if update_callback:
        entry.bind("<KeyRelease>", update_callback)
    
    return entry

# Callback to update json_data when the entry value changes
def update_json_data(event):
    """ Update json_data when an entry value is modified. """
    json_data['dictionaryOfDictionaries']['value']['runStats']['currency'] = int(entry_currency.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['lives'] = int(entry_lives.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'] = int(entry_charging.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'] = int(entry_haul.get())

    # Update the JSON viewer
    textbox.delete("1.0", "end")
    textbox.insert("1.0", json.dumps(json_data, indent=4))
    highlight_json()

entry_currency = create_entry("Currency:", frame_world, "#292929", update_json_data)
entry_lives = create_entry("Lives:", frame_world, "#292929", update_json_data)
entry_charging = create_entry("Charging Station Charge's:", frame_world, "#292929", update_json_data)
entry_haul = create_entry("Total Haul:", frame_world, "#292929", update_json_data)

entry_currency.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['currency'])
entry_lives.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['lives'])
entry_charging.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])
entry_haul.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])

frame_items = CTkFrame(frame_world, corner_radius=10)
frame_items.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_items, text="Items", font=font).pack(anchor="w", padx=10, pady=5)
CTkLabel(frame_items, text="Coming Soon", font=font, text_color="white").pack(fill=BOTH, expand=True)

# ========== Player Tab ========== 
frame_player = CTkFrame(tabview.tab("Player"))
frame_player.pack(fill=BOTH, expand=True, padx=10, pady=10)

player_entries = {}

def fetch_steam_profile_picture(player_id):
    """Fetch and cache Steam profile picture in the cache folder."""
    cached_image_path = CACHE_DIR / f"{player_id}.png"
    if cached_image_path.exists():
        return str(cached_image_path)  # Return cached image if available

    url = f"https://steamcommunity.com/profiles/{player_id}/?xml=1"
    response = requests.get(url)
    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)
        avatar_icon = tree.find('avatarIcon')
        if avatar_icon is not None:
            img_url = avatar_icon.text
            img_data = requests.get(img_url).content
            with open(cached_image_path, 'wb') as file:
                file.write(img_data)
            return str(cached_image_path)  # Return the cached file path

    return "example.png"  # Default profile picture

def fetch_playerdata():
    """ Fetch player data from the JSON data. """
    fetched_players = {}
    for player_id, player_name in json_data["playerNames"]["value"].items():
        fetched_players[player_id] = player_name

    # Save the fetched_players dictionary back to the JSON data
    json_data["playerNames"]["value"] = fetched_players

    for player_id, player_name in fetched_players.items():
        player_health = json_data.get("playerHealth", {}).get(player_id, 100)  # Default health to 100 if not found
        players.append({"id": player_id, "name": player_name, "health": player_health})
    
    print(players)

fetch_playerdata()

for player in players:
    frame = CTkFrame(frame_player, corner_radius=6)
    frame.pack(fill="x", pady=3)

    profile_picture_path = fetch_steam_profile_picture(player['id'])

    image = Image.open(profile_picture_path)
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
    """ Updates JSON and applies highlighting. Also updates the entries accordingly. """
    try:
        updated_data = json.loads(textbox.get("1.0", "end-1c"))
        global json_data
        json_data = updated_data  # Update the json_data with the new data from the JSON editor.

        # Update UI entries based on the updated json_data
        entry_currency.delete(0, "end")
        entry_lives.delete(0, "end")
        entry_charging.delete(0, "end")
        entry_haul.delete(0, "end")

        entry_currency.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['currency'])
        entry_lives.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['lives'])
        entry_charging.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])
        entry_haul.insert(0, json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])

        highlight_json()  # Reapply syntax highlighting

    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)

frame_advanced = CTkFrame(tabview.tab("Advanced"))
frame_advanced.pack(fill=BOTH, expand=True, padx=10, pady=10)
CTkLabel(frame_advanced, text="Edit JSON:", font=font).pack(anchor="w", padx=5, pady=3)

textbox = Text(frame_advanced, font=("Courier", 10), height=12, wrap="word", bg="#2b2b2b", fg="white", insertbackground="white")
textbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
textbox.bind("<KeyRelease>", update_json)
textbox.insert("1.0", json.dumps(json_data, indent=4))

textbox.tag_configure("key", foreground="#FFCC00")      # Yellow for keys
textbox.tag_configure("string", foreground="#99CC99")   # Green for strings
textbox.tag_configure("number", foreground="#FF6666")   # Red for numbers
textbox.tag_configure("boolean", foreground="#66CCFF")  # Blue for booleans

highlight_json()

# ========== Save/Load Functions ==========

def open_file():
    """ Open a file dialog and load JSON data. """
    global file, json_data
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        file = file_path
        with open(file, 'r') as f:
            json_data = json.load(f)
            update_ui_from_json(json_data)

def save_data():
    """ Save the current data to a file. """
    if file:
        with open(file, 'w') as f:
            json.dump(json_data, f, indent=4)
            print("Data saved to", file)
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(json_data, f, indent=4)
                print("Data saved to", file_path)

def update_ui_from_json(data):
    """ Update UI from loaded JSON data. """
    entry_currency.delete(0, "end")
    entry_lives.delete(0, "end")
    entry_charging.delete(0, "end")
    entry_haul.delete(0, "end")

    entry_currency.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['currency'])
    entry_lives.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['lives'])
    entry_charging.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])
    entry_haul.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])


# ========== Footer ==========
label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
label_footer.pack(side="bottom", pady=5)

root.mainloop()