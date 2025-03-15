from customtkinter import *
from tkinter import TOP, X, BOTH
from lib.CTkMenuBar import *
from datetime import datetime
import json

version = "1.0.0"
file = None
players = [
    {
        'name': 'Player 1',
        'health': 100,
    },
    {
        'name': 'Player 2',
        'health': 100,
    }
]

root  = CTk()
root.geometry("690x440")
root.title("R.E.P.O Save Editor")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")
# Font settings
font = ("Arial", 14)
small_font = ("Arial", 10)
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
tabview.pack(fill=BOTH, expand=1)
tabview.add("World")
tabview.add("Player")
tabview.add("Advanced")

tabview.grid(row=0, column=0, padx=5, pady=5)

label_1 = CTkLabel(tabview.tab("World"), text="Balance: ", font=font)
label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_1 = CTkEntry(tabview.tab("World"), font=font)
entry_1.grid(row=0, column=1, padx=20, pady=5, sticky="e")

label_2 = CTkLabel(tabview.tab("World"), text="Currency: ", font=font)
label_2.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_2 = CTkEntry(tabview.tab("World"), font=font)
entry_2.grid(row=1, column=1, padx=20, pady=5, sticky="e")

label_3 = CTkLabel(tabview.tab("World"), text="Lives: ", font=font)
label_3.grid(row=2, column=0, padx=10, pady=5, sticky="w")

entry_3 = CTkEntry(tabview.tab("World"), font=font)
entry_3.grid(row=2, column=1, padx=20, pady=5, sticky="e")

label_4 = CTkLabel(tabview.tab("World"), text="Charging Station Charge's: ", font=font)
label_4.grid(row=0, column=3, padx=10, pady=5, sticky="w")

entry_4 = CTkEntry(tabview.tab("World"), font=font)
entry_4.grid(row=0, column=4, padx=20, pady=5, sticky="e")

label_5 = CTkLabel(tabview.tab("World"), text="Total Haul: ", font=font)
label_5.grid(row=1, column=3, padx=10, pady=5, sticky="w")

entry_5 = CTkEntry(tabview.tab("World"), font=font)
entry_5.grid(row=1, column=4, padx=20, pady=5, sticky="e")

# Frame Items
frame_items = CTkFrame(tabview.tab("World"), width=680, height=300, corner_radius=10)
frame_items.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="we")

label_items_title = CTkLabel(frame_items, text="Items", font=font)
label_items_title.pack(anchor="w", padx=10, pady=5)
frame_items.grid_propagate(False)
# Inner Frame
inner_frame = CTkFrame(frame_items, width=680, height=300, fg_color="gray20", corner_radius=10)
inner_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

label_coming_soon = CTkLabel(inner_frame, text="Coming Soon", font=font, text_color="white")
label_coming_soon.pack(fill=BOTH, expand=True)

class MyCheckboxFrame(CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


# Make a frame for each player
player_frames = []
for i, player in enumerate(players):
    frame = CTkFrame(tabview.tab("Player"), fg_color="gray20", corner_radius=6)
    frame.grid(row=i//2, column=i%2, padx=10, pady=(10, 0), sticky="ew")
    player_frames.append(frame)
    
    title = CTkLabel(frame, text=player['name'], fg_color="gray30", corner_radius=6)
    title.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
    
    health_label = CTkLabel(frame, text=f"Health: {player['health']}", fg_color="gray30", corner_radius=6)
    health_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

def update_json(event):
    try:
        data = json.loads(textbox.get("1.0", "end-1c"))
        print("JSON updated:", data)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)

label_json = CTkLabel(tabview.tab("Advanced"), text="Edit JSON:", font=font)
label_json.grid(row=0, column=0, padx=10, pady=5, sticky="w")

textbox = CTkTextbox(tabview.tab("Advanced"), width=656, height=300, font=("Courier", 12))
textbox.grid(row=1, column=0, padx=5, pady=5, sticky="we")
textbox.bind("<KeyRelease>", update_json)

# Load initial JSON data
initial_data = json.dumps(players, indent=4)
textbox.insert("1.0", initial_data)


label_footer = CTkLabel(root, text=f"Version: {version}, Copyright © {datetime.now().year} noedl.xyz", font=small_font, text_color="gray30")
label_footer.grid(row=1, column=0, padx=15, sticky="e")

root.mainloop()