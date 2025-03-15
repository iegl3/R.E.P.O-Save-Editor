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

    save_json(data)
    messagebox.showinfo("Succes", "Gegevens opgeslagen!")

def create_ui():
    global entry_level, entry_currency, entry_lives, entry_health  # Declare these as global to use them in update_run_stats
    
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

    # Player Tab UI (dynamic for each player)
    row = 0  # Start from the first row for player health
    entry_health = {}  # Dictionary to store the entry fields for health
    for player_id, player_name in data['playerNames']['value'].items():
        tk.Label(player_tab, text=f"{player_name} Health:").grid(row=row, column=0, padx=10, pady=5)
        entry_health[player_id] = tk.Entry(player_tab)
        entry_health[player_id].insert(0, str(data['dictionaryOfDictionaries']['value']['playerHealth'][player_id]))
        entry_health[player_id].grid(row=row, column=1, padx=10, pady=5)
        row += 1

    # Advanced Tab UI
    tk.Label(advanced_tab, text="Advanced Settings").grid(row=0, column=0, padx=10, pady=5)
    # You can add more advanced settings here

    # Save button
    btn_save = tk.Button(root, text="Opslaan", command=update_run_stats)
    btn_save.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    data = load_json()
    create_ui()
