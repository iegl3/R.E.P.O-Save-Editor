import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

def load_json():
    with open("save.json", "r") as file:
        data = json.load(file)
    return data  # Dit kan worden vervangen door het laden van een bestand

def save_json(data):
    # Dit kan worden vervangen door het opslaan naar een bestand
    with open("save.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print("Data opgeslagen:", json.dumps(data, indent=4))

def update_run_stats():
    level = int(entry_level.get())
    currency = int(entry_currency.get())
    lives = int(entry_lives.get())  # Get the value from the health (lives) input field
    
    data['dictionaryOfDictionaries']['value']['runStats']['level'] = level
    data['dictionaryOfDictionaries']['value']['runStats']['currency'] = currency
    data['dictionaryOfDictionaries']['value']['runStats']['lives'] = lives  # Update the lives value
    
    # Save the player health using the ID
    for player_id, player_name in data['playerNames']['value'].items():
        player_health = int(entry_health[player_id].get())  # Get the health for each player
        data['dictionaryOfDictionaries']['value']['playerHealth'][player_id] = player_health

        # Save the player upgrades
        data['dictionaryOfDictionaries']['value']['playerUpgradeHealth'][player_id] = int(entry_upgrade_health[player_id].get())
        data['dictionaryOfDictionaries']['value']['playerUpgradeStamina'][player_id] = int(entry_upgrade_stamina[player_id].get())
        data['dictionaryOfDictionaries']['value']['playerUpgradeExtraJump'][player_id] = int(entry_upgrade_extra_jump[player_id].get())

    save_json(data)
    messagebox.showinfo("Succes", "Gegevens opgeslagen!")

def create_ui():
    global entry_level, entry_currency, entry_lives, entry_health, entry_upgrade_health, entry_upgrade_stamina, entry_upgrade_extra_jump  # Declare all as global to use them in update_run_stats
    
    root = tk.Tk()
    root.title("JSON Editor")

    # Create a Notebook (tabs container)
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, padx=10, pady=5)

    # Create frames for each tab
    game_tab = ttk.Frame(notebook)
    player_tab = ttk.Frame(notebook)
    advanced_tab = ttk.Frame(notebook)

    # Add frames as tabs
    notebook.add(game_tab, text="Game")
    notebook.add(player_tab, text="Player")
    notebook.add(advanced_tab, text="Advanced")

    # Game Tab UI
    tk.Label(game_tab, text="Level:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(game_tab, text="Currency:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(game_tab, text="Lives (Health):").grid(row=2, column=0, padx=10, pady=5)

    entry_level = tk.Entry(game_tab)
    entry_level.insert(0, str(data['dictionaryOfDictionaries']['value']['runStats']['level']))
    entry_level.grid(row=0, column=1, padx=10, pady=5)

    entry_currency = tk.Entry(game_tab)
    entry_currency.insert(0, str(data['dictionaryOfDictionaries']['value']['runStats']['currency']))
    entry_currency.grid(row=1, column=1, padx=10, pady=5)

    entry_lives = tk.Entry(game_tab)  # New entry field for health
    entry_lives.insert(0, str(data['dictionaryOfDictionaries']['value']['runStats']['lives']))
    entry_lives.grid(row=2, column=1, padx=10, pady=5)

    # Player Tab UI
    player_frame = tk.Frame(player_tab)
    player_frame.grid(row=0, column=0, padx=10, pady=5)

    # Create a collapsible frame for Health, Stamina, and Upgrades
    def create_collapsible_frame(parent, label, content_frame):
        # Label to toggle the frame
        frame_label = tk.Label(parent, text=label, relief="sunken", cursor="hand2")
        frame_label.pack(fill="x", padx=5, pady=5)
        
        # Toggle frame visibility on label click
        def toggle_frame():
            if content_frame.winfo_ismapped():
                content_frame.pack_forget()
            else:
                content_frame.pack(fill="x", padx=5, pady=5)
        
        frame_label.bind("<Button-1>", lambda event: toggle_frame())

        return content_frame

    # Health Section
    health_content_frame = tk.Frame(player_frame)
    health_content_frame = create_collapsible_frame(player_frame, "Health", health_content_frame)
    
    entry_health = {}  # Dictionary to store the entry fields for health
    for player_id, player_name in data['playerNames']['value'].items():
        tk.Label(health_content_frame, text=f"{player_name} Health:").pack(side="top", anchor="w", padx=10, pady=5)
        entry_health[player_id] = ttk.Combobox(health_content_frame, values=[str(i) for i in range(0, 201)])  # Health values between 0 and 200
        entry_health[player_id].set(str(data['dictionaryOfDictionaries']['value']['playerHealth'][player_id]))  # Set default value
        entry_health[player_id].pack(side="top", fill="x", padx=10, pady=5)

    # Stamina Section
    stamina_content_frame = tk.Frame(player_frame)
    stamina_content_frame = create_collapsible_frame(player_frame, "Stamina", stamina_content_frame)
    
    entry_upgrade_stamina = {}  # Dictionary to store the entry fields for stamina
    for player_id, player_name in data['playerNames']['value'].items():
        tk.Label(stamina_content_frame, text=f"{player_name} Stamina:").pack(side="top", anchor="w", padx=10, pady=5)
        entry_upgrade_stamina[player_id] = tk.Entry(stamina_content_frame)
        entry_upgrade_stamina[player_id].insert(0, str(data['dictionaryOfDictionaries']['value']['playerUpgradeStamina'][player_id]))
        entry_upgrade_stamina[player_id].pack(side="top", fill="x", padx=10, pady=5)

    # Extra Jump Section
    extra_jump_content_frame = tk.Frame(player_frame)
    extra_jump_content_frame = create_collapsible_frame(player_frame, "Extra Jump", extra_jump_content_frame)
    
    entry_upgrade_extra_jump = {}  # Dictionary to store the entry fields for extra jump
    for player_id, player_name in data['playerNames']['value'].items():
        tk.Label(extra_jump_content_frame, text=f"{player_name} Extra Jump:").pack(side="top", anchor="w", padx=10, pady=5)
        entry_upgrade_extra_jump[player_id] = tk.Entry(extra_jump_content_frame)
        entry_upgrade_extra_jump[player_id].insert(0, str(data['dictionaryOfDictionaries']['value']['playerUpgradeExtraJump'][player_id]))
        entry_upgrade_extra_jump[player_id].pack(side="top", fill="x", padx=10, pady=5)

    # Save button
    btn_save = tk.Button(root, text="Opslaan", command=update_run_stats)
    btn_save.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    data = load_json()
    create_ui()
