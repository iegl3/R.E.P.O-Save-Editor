from customtkinter import *
from tkinter import BOTH, Text, Toplevel, filedialog, messagebox
from lib.CTkMenuBar import *
from lib.CTkToolTip import *
from decrypt import decrypt_es3
from encrypt import encrypt_es3
from datetime import datetime
import json
import re
import requests
from xml.etree import ElementTree
from PIL import Image
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "noedl.xyz"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

print(CACHE_DIR)

version = "1.0.0"
json_data = {}

root = CTk()
root.geometry("900x540")
root.title("R.E.P.O Save Editor")
root.iconbitmap("icon.ico")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

font = ("Arial", 12)
small_font = ("Arial", 9)

menu = CTkTitleMenu(master=root)
button_file = menu.add_cascade("File")
dropdown1 = CustomDropdownMenu(widget=button_file)
dropdown1.add_option(option="Open", command=lambda: open_file())

label = CTkLabel(root, text="No data loaded.", font=font)
label.pack(fill=BOTH, expand=True)

def get_latest_version():
    try:
        response = requests.get(f"https://api.github.com/repos/N0edL/R.E.P.O-Save-Editor/releases/latest", timeout=5)
        data = response.json()
        return data.get("tag_name", "Unknown")
    except requests.exceptions.RequestException:
        return "Unknown"

if get_latest_version() != version:
    if get_latest_version() == "Unknown":
        label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
    else:
        label_footer = CTkLabel(root, text=f"Version: {version} (Latest: {get_latest_version()}), Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
else:
    label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
label_footer.pack(side="bottom", pady=5)

players = []
player_entries = {}

def create_entry(label, parent, color, update_callback=None, tooltip=None):
    frame = CTkFrame(parent, fg_color=color)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=label, font=font).pack(side="left", padx=5)
    entry = CTkEntry(frame, font=font, width=100, border_color='#303030', fg_color="#292929")
    entry.pack(side="right", padx=5)
    if tooltip:
        CTkToolTip(frame, tooltip)
    if update_callback:
        entry.bind("<KeyRelease>", update_callback)
    return entry

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

def update_json_data(event):
    json_data['dictionaryOfDictionaries']['value']['runStats']['level'] = int(entry_level.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['currency'] = int(entry_currency.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['lives'] = int(entry_lives.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'] = int(entry_charging.get())
    json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'] = int(entry_haul.get())
    json_data['teamName']['value'] = entry_teamname.get()
    for player in players:
        player['health'] = int(player_entries[player['name']].get())
        json_data['dictionaryOfDictionaries']['value']['playerHealth'][player['id']] = player['health']
    textbox.delete("1.0", "end")
    textbox.insert("1.0", json.dumps(json_data, indent=4))
    highlight_json()

def on_json_edit(event):
    """ Updates the UI fields when the JSON editor is modified. """
    global json_data
    try:
        updated_data = json.loads(textbox.get("1.0", "end-1c"))

        entry_level.delete(0, "end")
        entry_level.insert(0, updated_data['dictionaryOfDictionaries']['value']['runStats']['level'])

        entry_currency.delete(0, "end")
        entry_currency.insert(0, updated_data['dictionaryOfDictionaries']['value']['runStats']['currency'])

        entry_lives.delete(0, "end")
        entry_lives.insert(0, updated_data['dictionaryOfDictionaries']['value']['runStats']['lives'])

        entry_charging.delete(0, "end")
        entry_charging.insert(0, updated_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])

        entry_haul.delete(0, "end")
        entry_haul.insert(0, updated_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])

        entry_teamname.delete(0, "end")
        entry_teamname.insert(0, updated_data['teamName']['value'])

        for player in players:
            player_name = player['name']
            player_id = player['id']  # This should match the Steam ID in the JSON

            # Make sure the player ID exists in the JSON data
            if player_id in updated_data['dictionaryOfDictionaries']['value']['playerHealth']:
                health_value = updated_data['dictionaryOfDictionaries']['value']['playerHealth'][player_id]

                # Ensure the UI entry exists before modifying it
                if f"{player_name}_health" in player_entries:
                    player_entries[f"{player_name}_health"].delete(0, "end")
                    player_entries[f"{player_name}_health"].insert(0, health_value)
                    
        json_data = updated_data
        highlight_json()

    except json.JSONDecodeError:
        pass

def open_file():
    global json_data
    file_path = filedialog.askopenfilename(filetypes=[("Game Save (.es3 file)", "*.es3")])
    if file_path:        
        decrypted_data = decrypt_es3(file_path, "Why would you want to cheat?... :o It's no fun. :') :'D")
        json_data = json.loads(decrypted_data)
        update_ui_from_json(json_data)
        messagebox.showinfo("File Opened", f"Successfully opened: {file_path}")

def save_data():
    if not json_data:
        messagebox.showerror("Error", "No data to save.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".es3", filetypes=[("Game Save (.es3 file)", "*.es3")])
    if file_path:
        encrypted_data = encrypt_es3(json.dumps(json_data, indent=4).encode('utf-8'), "Why would you want to cheat?... :o It's no fun. :') :'D")
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        messagebox.showinfo("File Saved", f"Successfully saved: {file_path}")

def update_ui_from_json(data):
    global players, player_entries
    players.clear()
    player_entries.clear()

    dropdown1.add_option(option="Save", command=lambda: save_data())
    dropdown1.add_separator()
    sub_menu = dropdown1.add_submenu("Export As (Currently Unavailable)")
    sub_menu.add_option(option=".TXT (Currently Unavailable)", command=lambda: messagebox.showinfo("Error", "I told you it's not available yet. :)"))
    sub_menu.add_option(option=".JSON (Currently Unavailable)", command=lambda: messagebox.showinfo("Error", "I told you it's not available yet. :)"))
    
    tabview = CTkTabview(root, width=680, height=400)
    tabview.pack(fill=BOTH, expand=True)
    tabview.add("World")
    tabview.add("Player")
    tabview.add("Advanced")
    
    frame_world = CTkFrame(tabview.tab("World"))
    frame_world.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    global entry_level, entry_currency, entry_lives, entry_charging, entry_haul, entry_teamname
    entry_level = create_entry("Level:", frame_world, "#292929", update_json_data, "The level of the game.")
    entry_currency = create_entry("Currency:", frame_world, "#292929", update_json_data, "The amount of currency the game has. In thousands.")
    entry_lives = create_entry("Lives:", frame_world, "#292929", update_json_data, "The amount of lives the game has.")
    entry_charging = create_entry("Charging Station Charge's:", frame_world, "#292929", update_json_data, "The amount of charge the charging station has.")
    entry_haul = create_entry("Total Haul:", frame_world, "#292929", update_json_data, "The total haul of the game.")
    entry_teamname = create_entry("Team Name:", frame_world, "#292929", update_json_data, "The name of the team.")

    entry_level.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['level'])
    entry_currency.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['currency'])
    entry_lives.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['lives'])
    entry_charging.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])
    entry_haul.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])
    entry_teamname.insert(0, data['teamName']['value'])

    frame_items = CTkFrame(frame_world, corner_radius=10)
    frame_items.pack(fill=BOTH, expand=True, pady=10)
    CTkLabel(frame_items, text="Items", font=font).pack(anchor="w", padx=10, pady=5)
    CTkLabel(frame_items, text="Coming Soon", font=font, text_color="white").pack(fill=BOTH, expand=True)
    
    frame_player = CTkScrollableFrame(tabview.tab("Player"))
    frame_player.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    for player_id, player_name in data["playerNames"]["value"].items():
        player_health = data["dictionaryOfDictionaries"]["value"]["playerHealth"][player_id]
        players.append({"id": player_id, "name": player_name, "health": player_health})
    
    def fetch_steam_profile_picture(player_id):
        """Fetch and cache Steam profile picture in the cache folder."""
        cached_image_path = CACHE_DIR / f"{player_id}.png"
        if cached_image_path.exists():
            return str(cached_image_path)

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
                return str(cached_image_path)

        return "https://media.discordapp.net/attachments/964544992251084890/1350830278763085844/R.E.P.O_Save_Editor_icon.png?ex=67d82a3b&is=67d6d8bb&hm=7d2ffdd5b03ec4d77f580901d3b73f36e999bc96bcab7a8535ff999a527f2596&="

    for player in players:
        frame = CTkFrame(frame_player, corner_radius=6, fg_color="#292929")
        frame.pack(fill="x", pady=3)

        profile_picture_path = fetch_steam_profile_picture(player['id'])

        image = Image.open(profile_picture_path)
        my_image = CTkImage(light_image=image, dark_image=image, size=(30, 30))
        image_label = CTkLabel(frame, image=my_image, text="")
        image_label.pack(side="left", anchor="nw", padx=(10, 5), pady=10)
        
        CTkLabel(frame, text=player['name'], font=font).pack(anchor="w", padx=5, pady=[5, 0])

        health_entry = create_entry("Health:", frame, "#292929", update_json_data, "The amount of health the player has. Max 200.")
        health_entry.insert(0, player['health'])
        player_entries[player['name']] = health_entry

        CTkLabel(frame, text="Upgrades: ", font=font).pack(anchor="w")        
        CTkFrame(frame, width=frame.winfo_width()-10, height=2, fg_color='gray25').pack(fill="x", pady=5)

        health_upgrade_entry = create_entry("Health:", frame, "#292929", update_json_data)
        health_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeHealth'][player['id']])
        player_entries[player['name']] = health_upgrade_entry

        stamina_upgrade_entry = create_entry("Stamina:", frame, "#292929", update_json_data)
        stamina_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeStamina'][player['id']])
        player_entries[player['name']] = stamina_upgrade_entry
        
        extra_jump_entry = create_entry("Extra Jump:", frame, "#292929", update_json_data)
        extra_jump_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeExtraJump'][player['id']])
        player_entries[player['name']] = extra_jump_entry

        lauch_upgrade_entry = create_entry("Launch:", frame, "#292929", update_json_data)
        lauch_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeLaunch'][player['id']])
        player_entries[player['name']] = lauch_upgrade_entry

        mapplayercount_upgrade_entry = create_entry("Map Player Count:", frame, "#292929", update_json_data)
        mapplayercount_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeMapPlayerCount'][player['id']])
        player_entries[player['name']] = mapplayercount_upgrade_entry

        speed_upgrade_entry = create_entry("Speed:", frame, "#292929", update_json_data)
        speed_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeSpeed'][player['id']])
        player_entries[player['name']] = speed_upgrade_entry

        strength_upgrade_entry = create_entry("Strength:", frame, "#292929", update_json_data)
        strength_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeStrength'][player['id']])
        player_entries[player['name']] = strength_upgrade_entry

        range_upgrade_entry = create_entry("Range:", frame, "#292929", update_json_data)
        range_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeRange'][player['id']])
        player_entries[player['name']] = range_upgrade_entry

        throw_upgrade_entry = create_entry("Throw:", frame, "#292929", update_json_data)
        throw_upgrade_entry.insert(0, data['dictionaryOfDictionaries']['value']['playerUpgradeThrow'][player['id']])
        player_entries[player['name']] = throw_upgrade_entry


    frame_advanced = CTkFrame(tabview.tab("Advanced"), corner_radius=10)
    frame_advanced.pack(fill=BOTH, expand=True, padx=10, pady=10)
    CTkLabel(frame_advanced, text="Edit JSON:", font=font).pack(anchor="w", padx=5, pady=3)
    
    global textbox
    textbox = Text(frame_advanced, font=("Courier", 10), height=12, wrap="word", bg="#2b2b2b", fg="white", bd=0, highlightthickness=0, insertbackground="white")
    textbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
    textbox.insert("1.0", json.dumps(json_data, indent=4))
    
    textbox.tag_configure("key", foreground="#e06c69")      # Keys
    textbox.tag_configure("string", foreground="#7ac379")   # Strings
    textbox.tag_configure("number", foreground="#d19a5d")   # Numbers
    textbox.tag_configure("boolean", foreground="#66CCFF")  # Booleans

    highlight_json()
    textbox.bind("<KeyRelease>", on_json_edit)
    label.pack_forget()

root.mainloop()