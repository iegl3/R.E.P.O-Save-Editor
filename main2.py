import json
from tabulate import tabulate

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def display_table(data):
    """Display a table of player names, IDs, and HP."""
    player_health = data["dictionaryOfDictionaries"]["value"]["playerHealth"]
    player_names = data["playerNames"]["value"]
    
    table = []
    for player_id, hp in player_health.items():
        name = player_names.get(player_id, "Unknown")
        table.append([name, player_id, hp])
    
    print(tabulate(table, headers=["Name", "ID", "HP"], tablefmt="pretty"))

def update_player_hp(data):
    """Update a player's HP by their name."""
    player_health = data["dictionaryOfDictionaries"]["value"]["playerHealth"]
    player_names = data["playerNames"]["value"]
    
    display_table(data)
    
    # Ask for the player's name
    player_name = input("Enter the player's name to update their HP: ").strip()
    
    # Find the player ID(s) matching the name
    matching_ids = [player_id for player_id, name in player_names.items() if name == player_name]
    
    if not matching_ids:
        print(f"No player found with the name '{player_name}'!")
        return
    
    # If multiple players have the same name, let the user choose
    if len(matching_ids) > 1:
        print(f"Multiple players found with the name '{player_name}':")
        for i, player_id in enumerate(matching_ids):
            print(f"{i + 1}. ID: {player_id}, HP: {player_health[player_id]}")
        choice = input("Enter the number of the player you want to update: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matching_ids):
            print("Invalid choice!")
            return
        player_id = matching_ids[int(choice) - 1]
    else:
        player_id = matching_ids[0]
    
    # Update the player's HP
    new_hp = input(f"Enter new HP for {player_name}: ").strip()
    if not new_hp.isdigit():
        print("Invalid HP value! Please enter a number.")
        return
    
    player_health[player_id] = int(new_hp)
    print(f"HP for {player_name} (ID: {player_id}) updated to {new_hp}!")

def main():
    file_path = input("Enter the path to the JSON file: ").strip()
    data = load_json(file_path)
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Display Player Table")
        print("2. Update Player HP by Name")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            print("\033[H\033[J")
            display_table(data)
        elif choice == "2":
            print("\033[H\033[J")
            update_player_hp(data)
        elif choice == "3":
            save_json(file_path, data)
            print("Changes saved. Exiting...")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    main()