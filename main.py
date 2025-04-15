import json, re, requests, webbrowser, platform, os, sys, threading
from customtkinter import *
from tkinter import BOTH, Text, Toplevel, filedialog, messagebox
from lib.CTkMenuBar import *
from lib.CTkToolTip import *
from lib.decrypt import decrypt_es3
from lib.encrypt import encrypt_es3
from datetime import datetime
from xml.etree import ElementTree
from PIL import Image
from pathlib import Path

DEBUGLEVEL = None

if DEBUGLEVEL:
    import logging
    logging.basicConfig(level=DEBUGLEVEL)
    ui_logger = logging.getLogger("customtkinter")
    ui_logger.setLevel(DEBUGLEVEL)
    logger = logging.getLogger(__name__)
    logger.setLevel(DEBUGLEVEL)

CACHE_DIR = Path.home() / ".cache" / "noedl.xyz"
CACHE_DIR.mkdir(parents=True, exist_ok=True) 

if DEBUGLEVEL:
    logger.info("Cache directory created.")

version = "1.0.0"
json_data = {}
savefile_dir = None

# Set the save file directory based on OS
if platform.system() == "Windows":
    savefile_dir = Path.home() / "AppData" / "LocalLow" / "semiwork" / "Repo" / "saves"
elif platform.system() == "Darwin":  # macOS
    savefile_dir = Path.home() / "Library" / "Application Support" / "semiwork" / "Repo" / "saves"
elif platform.system() == "Linux":
    savefile_dir = Path.home() / ".local" / "share" / "semiwork" / "Repo" / "saves"

# Create custom saves directory if it doesn't exist
custom_saves_dir = Path.home() / "Documents" / "REPO_SaveEditor" / "saves"
custom_saves_dir.mkdir(parents=True, exist_ok=True)

if DEBUGLEVEL:
    logger.info("Save file directory set. Path: " + str(savefile_dir))
    logger.info("Custom saves directory set. Path: " + str(custom_saves_dir))

# Encryption key - moved to a variable for easier management
ENCRYPTION_KEY = "Why would you want to cheat?... :o It's no fun. :') :'D"

def resource_path(relative_path):
    """ Get the absolute path to resources (for PyInstaller compatibility) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

root = CTk()
root.geometry("900x540")
root.title("R.E.P.O Save Editor")
root.iconbitmap("icon.ico")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

font = ("Arial", 12)
small_font = ("Arial", 9)

if platform.system() == "Windows":
    menu = CTkTitleMenu(master=root)
else:
    menu = CTkMenuBar(master=root)

button_file = menu.add_cascade("File")
button_help = menu.add_cascade("Help")
dropdown1 = CustomDropdownMenu(widget=button_file)
dropdown1.add_option(option="Open", command=lambda: open_file())
dropdown2 = CustomDropdownMenu(widget=button_help)

dropdown2.add_option(option="How to Use", command=lambda: webbrowser.open("https://github.com/N0edL/R.E.P.O-Save-Editor#how-to-use"))
dropdown2.add_option(option="About", command=lambda: webbrowser.open("https://github.com/N0edL/R.E.P.O-Save-Editor"))
dropdown2.add_option(option="Report Issue", command=lambda: webbrowser.open("https://github.com/N0edL/R.E.P.O-Save-Editor/issues/new"))

label = CTkLabel(root, text="No data loaded.", font=font)
label.pack(fill=BOTH, expand=True)

def get_latest_version():
    try:
        response = requests.get(f"https://api.github.com/repos/N0edL/R.E.P.O-Save-Editor/releases/latest", timeout=5)
        data = response.json()
        if DEBUGLEVEL:
            logger.info("Latest version fetched from GitHub API. Version: " + data.get("tag_name", "Unknown"))
        return data.get("tag_name", "Unknown")
    except requests.exceptions.RequestException:
        if DEBUGLEVEL:
            logger.error("Failed to fetch latest version from GitHub API.")
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

def create_entry(label, parent, color, update_callback=None, tooltip=None, numeric_only=False):
    frame = CTkFrame(parent, fg_color=color)
    frame.pack(fill="x", pady=3)
    CTkLabel(frame, text=label, font=font).pack(side="left", padx=5)
    entry = CTkEntry(frame, font=font, width=100, border_color='#303030', fg_color="#292929")
    entry.pack(side="right", padx=5)
    if tooltip:
        CTkToolTip(frame, tooltip)
    
    if numeric_only:
        def validate_numeric(event):
            value = entry.get()
            if value and not value.isdigit():
                entry.delete(0, "end")
                entry.insert(0, ''.join(filter(str.isdigit, value)) or "0")
            if update_callback:
                update_callback(event)
        entry.bind("<KeyRelease>", validate_numeric)
    elif update_callback:
        entry.bind("<KeyRelease>", update_callback)
    
    if DEBUGLEVEL:
        ui_logger.info(f"Creating entry field for: {label}")
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
        
        if DEBUGLEVEL:
            ui_logger.info("JSON syntax highlighted.")

def update_json_data(event):
    try:
        if not all(e.get() for e in [entry_level, entry_currency, entry_lives, entry_charging, entry_haul, entry_teamname]):
            if DEBUGLEVEL:
                ui_logger.info("Failed to update JSON data. One or more fields are empty.")
            return
        
        # Convert string values to appropriate types with error handling
        json_data['dictionaryOfDictionaries']['value']['runStats']['level'] = int(entry_level.get() or 0)
        json_data['dictionaryOfDictionaries']['value']['runStats']['currency'] = int(entry_currency.get() or 0)
        json_data['dictionaryOfDictionaries']['value']['runStats']['lives'] = int(entry_lives.get() or 0)
        json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'] = int(entry_charging.get() or 0)
        json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'] = int(entry_haul.get() or 0)
        json_data['teamName']['value'] = entry_teamname.get()
        
        for player in players:
            player_name = player['name']
            player_id = player['id']
            
            # Update player health with validation
            if f"{player_name}_health" in player_entries and player_entries[f"{player_name}_health"].get():
                try:
                    json_data["dictionaryOfDictionaries"]["value"]["playerHealth"][player_id] = int(player_entries[f"{player_name}_health"].get() or 0)
                except ValueError:
                    if DEBUGLEVEL:
                        ui_logger.error(f"Invalid health value for {player_name}")
            
            # Update player upgrades with validation
            for upgrade_type in ["health_upgrade", "stamina_upgrade", "extra_jump_upgrade", "launch_upgrade", 
                               "mapplayercount_upgrade", "speed_upgrade", "strength_upgrade", "range_upgrade", "throw_upgrade"]:
                key = f"{player_name}_{upgrade_type}"
                json_key = f"playerUpgrade{upgrade_type.split('_')[0].capitalize()}"
                if upgrade_type == "mapplayercount_upgrade":
                    json_key = "playerUpgradeMapPlayerCount"
                
                if key in player_entries and player_entries[key].get():
                    try:
                        json_data["dictionaryOfDictionaries"]["value"][json_key][player_id] = int(player_entries[key].get() or 0)
                    except (ValueError, KeyError) as e:
                        if DEBUGLEVEL:
                            ui_logger.error(f"Error updating {key}: {str(e)}")
        
        textbox.delete("1.0", "end")
        textbox.insert("1.0", json.dumps(json_data, indent=4))
        if DEBUGLEVEL:
            ui_logger.info("JSON data updated.")
            logger.info("JSON data updated successfully")
        highlight_json()
    except Exception as e:
        if DEBUGLEVEL:
            ui_logger.error(f"Error in update_json_data: {str(e)}")
        messagebox.showerror("Error", f"Failed to update JSON data: {str(e)}")

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
            player_id = player['id']

            print(f"Checking player: {player_name} (ID: {player_id})")

            if player_id in updated_data['dictionaryOfDictionaries']['value']['playerHealth']:
                health_value = updated_data['dictionaryOfDictionaries']['value']['playerHealth'][player_id]
                print(f"Health for {player_name}: {health_value}")

                if f"{player_name}_health" in player_entries:
                    print(f"Updating UI for {player_name}")
                    player_entries[f"{player_name}_health"].delete(0, "end")
                    player_entries[f"{player_name}_health"].insert(0, health_value)
                else:
                    print(f"Entry field missing for {player_name}_health")
            else:
                print(f"Player ID {player_id} not found in playerHealth")

        json_data = updated_data
        highlight_json()
    
        if DEBUGLEVEL:
            ui_logger.info("JSON data updated from editor.")
    except json.JSONDecodeError:
        if DEBUGLEVEL:
            ui_logger.error("Failed to update JSON data from editor.")
        pass

def open_file():
    global json_data, savefilename
    try:
        file_path = filedialog.askopenfilename(initialdir=savefile_dir, filetypes=[("Game Save (.es3 file)", "*.es3")])
        if not file_path:
            return
        
        # Show loading indicator
        label.configure(text="Loading file... Please wait.")
        root.update_idletasks()
        
        try:
            decrypted_data = decrypt_es3(file_path, ENCRYPTION_KEY)
            json_data = json.loads(decrypted_data)
            update_ui_from_json(json_data)
            savefilename = Path(file_path).name
            messagebox.showinfo("File Opened", f"Successfully opened: {file_path}")
            if DEBUGLEVEL:
                ui_logger.info(f"File opened: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the file: {str(e)}")
            if DEBUGLEVEL:
                ui_logger.error(f"Error opening file: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        if DEBUGLEVEL:
            ui_logger.error(f"Unexpected error in open_file: {str(e)}")

def save_data():
    global json_data, savefilename
    try:
        if not json_data:
            messagebox.showerror("Error", "No data to save.")
            if DEBUGLEVEL:
                ui_logger.error("No data to save.")
            return

        # Ask the user where to save
        default_dir = custom_saves_dir if custom_saves_dir.exists() else savefile_dir
        file_path = filedialog.asksaveasfilename(
            initialdir=default_dir, 
            initialfile=savefilename, 
            defaultextension=".es3", 
            filetypes=[("Game Save (.es3 file)", "*.es3")]
        )
        
        if not file_path:
            return
            
        # Show saving indicator
        label.configure(text="Saving file... Please wait.")
        root.update_idletasks()
            
        try:
            encrypted_data = encrypt_es3(json.dumps(json_data, indent=4).encode('utf-8'), ENCRYPTION_KEY)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
                
            # Create a backup copy in custom saves directory
            backup_path = custom_saves_dir / f"{Path(file_path).stem}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.es3"
            with open(backup_path, 'wb') as f:
                f.write(encrypted_data)
                
            messagebox.showinfo("File Saved", f"Successfully saved to:\n{file_path}\n\nBackup created at:\n{backup_path}")
            if DEBUGLEVEL:
                ui_logger.info(f"File saved: {file_path}")
                ui_logger.info(f"Backup created: {backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file: {str(e)}")
            if DEBUGLEVEL:
                ui_logger.error(f"Error saving file: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        if DEBUGLEVEL:
            ui_logger.error(f"Unexpected error in save_data: {str(e)}")

def export_as_json():
    """Export the current data as a JSON file."""
    if not json_data:
        messagebox.showerror("Error", "No data to export.")
        return
    
    file_path = filedialog.asksaveasfilename(
        initialdir=custom_saves_dir,
        initialfile=f"{Path(savefilename).stem if 'savefilename' in globals() else 'repo_save'}.json",
        defaultextension=".json",
        filetypes=[("JSON file", "*.json")]
    )
    
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
            messagebox.showinfo("Export Successful", f"Successfully exported to: {file_path}")
            if DEBUGLEVEL:
                ui_logger.info(f"Exported as JSON: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            if DEBUGLEVEL:
                ui_logger.error(f"Export error: {str(e)}")

def export_as_txt():
    """Export the current data as a formatted text file."""
    if not json_data:
        messagebox.showerror("Error", "No data to export.")
        return
    
    file_path = filedialog.asksaveasfilename(
        initialdir=custom_saves_dir,
        initialfile=f"{Path(savefilename).stem if 'savefilename' in globals() else 'repo_save'}.txt",
        defaultextension=".txt",
        filetypes=[("Text file", "*.txt")]
    )
    
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"R.E.P.O Save Data Export\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write(f"Team Name: {json_data['teamName']['value']}\n\n")
                
                f.write("Game Stats:\n")
                f.write(f"  Level: {json_data['dictionaryOfDictionaries']['value']['runStats']['level']}\n")
                f.write(f"  Currency: {json_data['dictionaryOfDictionaries']['value']['runStats']['currency']}\n")
                f.write(f"  Lives: {json_data['dictionaryOfDictionaries']['value']['runStats']['lives']}\n")
                f.write(f"  Charging Station: {json_data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge']}\n")
                f.write(f"  Total Haul: {json_data['dictionaryOfDictionaries']['value']['runStats']['totalHaul']}\n\n")
                
                f.write("Player Data:\n")
                for player in players:
                    player_id = player['id']
                    f.write(f"  Player: {player['name']} (ID: {player_id})\n")
                    f.write(f"    Health: {json_data['dictionaryOfDictionaries']['value']['playerHealth'].get(player_id, 'N/A')}\n")
                    f.write("    Upgrades:\n")
                    
                    upgrade_mapping = {
                        "Health": json_data['dictionaryOfDictionaries']['value']['playerUpgradeHealth'].get(player_id, 0),
                        "Stamina": json_data['dictionaryOfDictionaries']['value']['playerUpgradeStamina'].get(player_id, 0),
                        "Extra Jump": json_data['dictionaryOfDictionaries']['value']['playerUpgradeExtraJump'].get(player_id, 0),
                        "Launch": json_data['dictionaryOfDictionaries']['value']['playerUpgradeLaunch'].get(player_id, 0),
                        "Map Player Count": json_data['dictionaryOfDictionaries']['value']['playerUpgradeMapPlayerCount'].get(player_id, 0),
                        "Speed": json_data['dictionaryOfDictionaries']['value']['playerUpgradeSpeed'].get(player_id, 0),
                        "Strength": json_data['dictionaryOfDictionaries']['value']['playerUpgradeStrength'].get(player_id, 0),
                        "Range": json_data['dictionaryOfDictionaries']['value']['playerUpgradeRange'].get(player_id, 0),
                        "Throw": json_data['dictionaryOfDictionaries']['value']['playerUpgradeThrow'].get(player_id, 0)
                    }
                    
                    for upgrade_name, upgrade_value in upgrade_mapping.items():
                        f.write(f"      {upgrade_name}: {upgrade_value}\n")
                    f.write("\n")
                
            messagebox.showinfo("Export Successful", f"Successfully exported to: {file_path}")
            if DEBUGLEVEL:
                ui_logger.info(f"Exported as TXT: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            if DEBUGLEVEL:
                ui_logger.error(f"Export error: {str(e)}")

def update_ui_from_json(data):
    global players, player_entries
    players.clear()
    player_entries.clear()

    # Create menu options for loaded data
    dropdown1.add_option(option="Save", command=lambda: save_data())
    dropdown1.add_separator()
    sub_menu = dropdown1.add_submenu("Export As")
    sub_menu.add_option(option="Export as JSON", command=lambda: export_as_json())
    sub_menu.add_option(option="Export as TXT", command=lambda: export_as_txt())
    
    tabview = CTkTabview(root, width=680, height=400)
    tabview.pack(fill=BOTH, expand=True)
    tabview.add("World")
    tabview.add("Player")
    tabview.add("Advanced")
    
    # World tab setup
    frame_world = CTkFrame(tabview.tab("World"))
    frame_world.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    global entry_level, entry_currency, entry_lives, entry_charging, entry_haul, entry_teamname
    entry_level = create_entry("Level:", frame_world, "#292929", update_json_data, "The level of the game.", True)
    entry_currency = create_entry("Currency:", frame_world, "#292929", update_json_data, "The amount of currency the game has. In thousands.", True)
    entry_lives = create_entry("Lives:", frame_world, "#292929", update_json_data, "The amount of lives the game has.", True)
    entry_charging = create_entry("Charging Station Charge's:", frame_world, "#292929", update_json_data, "The amount of charge the charging station has.", True)
    entry_haul = create_entry("Total Haul:", frame_world, "#292929", update_json_data, "The total haul of the game.", True)
    entry_teamname = create_entry("Team Name:", frame_world, "#292929", update_json_data, "The name of the team.")

    try:
        entry_level.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['level'])
        entry_currency.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['currency'])
        entry_lives.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['lives'])
        entry_charging.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['chargingStationCharge'])
        entry_haul.insert(0, data['dictionaryOfDictionaries']['value']['runStats']['totalHaul'])
        entry_teamname.insert(0, data['teamName']['value'])
    except KeyError as e:
        if DEBUGLEVEL:
            ui_logger.error(f"Key error in data: {str(e)}")
        messagebox.showwarning("Data Issue", f"Some game data appears to be missing. The save file may be corrupted or from an incompatible version.")

    # Items section with "Coming Soon" label
    frame_items = CTkFrame(frame_world, corner_radius=10)
    frame_items.pack(fill=BOTH, expand=True, pady=10)
    CTkLabel(frame_items, text="Items", font=font).pack(anchor="w", padx=10, pady=5)
    CTkLabel(frame_items, text="Items feature is planned for a future update", font=font, text_color="gray60").pack(fill=BOTH, expand=True)
    
    # Player tab setup
    frame_player = CTkScrollableFrame(tabview.tab("Player"))
    frame_player.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Load players
    try:
        for player_id, player_name in data["playerNames"]["value"].items():
            player_health = data["dictionaryOfDictionaries"]["value"]["playerHealth"].get(player_id, 100)
            players.append({"id": player_id, "name": player_name, "health": player_health})
    except KeyError as e:
        if DEBUGLEVEL:
            ui_logger.error(f"Key error loading players: {str(e)}")
        messagebox.showwarning("Data Issue", f"Player data could not be loaded properly. The save file may be corrupted.")
        return
        
    # Create player UI elements
    player_creation_thread = threading.Thread(target=create_player_ui, args=(frame_player, data))
    player_creation_thread.daemon = True
    player_creation_thread.start()

    # Advanced tab setup
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

    if DEBUGLEVEL:
        ui_logger.info("UI updated from JSON data.")

def create_player_ui(frame_player, data):
    """Create player UI elements (moved to a separate function for threading)"""
    for player in players:
        frame = CTkFrame(frame_player, corner_radius=6, fg_color="#292929")
        frame.pack(fill="x", pady=3)

        profile_picture_path = fetch_steam_profile_picture(player['id'])

        try:
            image = Image.open(profile_picture_path)
            my_image = CTkImage(light_image=image, dark_image=image, size=(30, 30))
            image_label = CTkLabel(frame, image=my_image, text="")
            image_label.pack(side="left", anchor="nw", padx=(10, 5), pady=10)
        except Exception as e:
            if DEBUGLEVEL:
                ui_logger.error(f"Error loading profile image: {str(e)}")
            # Fallback to text-only display
            CTkLabel(frame, text="👤", font=("Arial", 16)).pack(side="left", anchor="nw", padx=(10, 5), pady=10)
        
        CTkLabel(frame, text=player['name'], font=font).pack(anchor="w", padx=5, pady=[5, 0])

        health_entry = create_entry("Health:", frame, "#292929", update_json_data, "The amount of health the player has. Max 200.", True)
        health_entry.insert(0, player['health'])
        player_entries[f"{player['name']}_health"] = health_entry

        CTkLabel(frame, text="Upgrades: ", font=font).pack(anchor="w")        
        CTkFrame(frame, width=frame.winfo_width()-10, height=2, fg_color='gray25').pack(fill="x", pady=5)

        try:
            # Define all upgrade fields with numeric validation
            upgrade_fields = [
                ("health_upgrade", "Health:", data['dictionaryOfDictionaries']['value']['playerUpgradeHealth'].get(player['id'], 0)),
                ("stamina_upgrade", "Stamina:", data['dictionaryOfDictionaries']['value']['playerUpgradeStamina'].get(player['id'], 0)),
                ("extra_jump_upgrade", "Extra Jump:", data['dictionaryOfDictionaries']['value']['playerUpgradeExtraJump'].get(player['id'], 0)),
                ("launch_upgrade", "Launch:", data['dictionaryOfDictionaries']['value']['playerUpgradeLaunch'].get(player['id'], 0)),
                ("mapplayercount_upgrade", "Map Player Count:", data['dictionaryOfDictionaries']['value']['playerUpgradeMapPlayerCount'].get(player['id'], 0)),
                ("speed_upgrade", "Speed:", data['dictionaryOfDictionaries']['value']['playerUpgradeSpeed'].get(player['id'], 0)),
                ("strength_upgrade", "Strength:", data['dictionaryOfDictionaries']['value']['playerUpgradeStrength'].get(player['id'], 0)),
                ("range_upgrade", "Range:", data['dictionaryOfDictionaries']['value']['playerUpgradeRange'].get(player['id'], 0)),
                ("throw_upgrade", "Throw:", data['dictionaryOfDictionaries']['value']['playerUpgradeThrow'].get(player['id'], 0))
            ]
            
            # Create all upgrade entry fields
            for upgrade_id, upgrade_label, upgrade_value in upgrade_fields:
                entry = create_entry(upgrade_label, frame, "#292929", update_json_data, None, True)
                entry.insert(0, upgrade_value)
                player_entries[f"{player['name']}_{upgrade_id}"] = entry
                
        except KeyError as e:
            if DEBUGLEVEL:
                ui_logger.error(f"Key error in player upgrades: {str(e)}")
            label = CTkLabel(frame, text="Error loading upgrades. The save file may be corrupted.", 
                           font=small_font, text_color="red")
            label.pack(fill="x", padx=10, pady=5)

        if DEBUGLEVEL:
            ui_logger.info(f"Player {player['name']} UI created.")

def fetch_steam_profile_picture(player_id):
    """Fetch and cache Steam profile picture in the cache folder."""
    cached_image_path = CACHE_DIR / f"{player_id}.png"
    default_image_path = resource_path("icon.ico")
    
    # Return cached image if it exists and is less than 24 hours old
    if cached_image_path.exists():
        file_age = datetime.now().timestamp() - cached_image_path.stat().st_mtime
        if file_age < 86400:  # 24 hours in seconds
            return str(cached_image_path)
        # Otherwise continue and refresh the cache

    # Create a loading indicator for the UI
    loading_label = CTkLabel(root, text=f"Fetching profile for {player_id}...", font=small_font)
    loading_label.pack(side="bottom", before=label_footer)
    root.update_idletasks()
    
    try:
        url = f"https://steamcommunity.com/profiles/{player_id}/?xml=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            try:
                tree = ElementTree.fromstring(response.content)
                avatar_icon = tree.find('avatarIcon')
                if avatar_icon is not None:
                    img_url = avatar_icon.text
                    img_response = requests.get(img_url, timeout=5)
                    if img_response.status_code == 200:
                        with open(cached_image_path, 'wb') as file:
                            file.write(img_response.content)
                        if DEBUGLEVEL:
                            ui_logger.info(f"Steam profile picture for player ID: {player_id} fetched and cached.")
                        loading_label.destroy()
                        return str(cached_image_path)
            except Exception as e:
                if DEBUGLEVEL:
                    ui_logger.error(f"Error parsing Steam profile XML: {str(e)}")
    except requests.exceptions.RequestException as e:
        if DEBUGLEVEL:
            ui_logger.error(f"Failed to fetch Steam profile picture for player ID: {player_id}: {str(e)}")
    
    # Clean up the loading indicator
    loading_label.destroy()
    
    # Create a local fallback image from the icon.ico if available, otherwise use the URL
    if os.path.exists(default_image_path):
        return default_image_path
    else:
        return "https://raw.githubusercontent.com/N0edL/R.E.P.O-Save-Editor/main/icon.ico"

root.mainloop()