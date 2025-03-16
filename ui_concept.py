from customtkinter import *
from tkinter import BOTH, Text, Toplevel, filedialog, messagebox, Scrollbar
from lib.CTkMenuBar import *
from lib.CTkToolTip import *
from datetime import datetime
import json
import re
import requests
from xml.etree import ElementTree
from PIL import Image, ImageTk
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "noedl.xyz"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def create_scrollable_frame(parent):
    canvas = CTkCanvas(parent)
    scrollbar = CTkScrollbar(parent, command=canvas.yview)
    scrollable_frame = CTkFrame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return scrollable_frame

def update_ui_from_json(data):
    global players, player_entries
    players.clear()
    player_entries.clear()
    
    tabview = CTkTabview(root, width=680, height=400)
    tabview.pack(fill=BOTH, expand=True)
    tabview.add("World")
    tabview.add("Player")
    tabview.add("Advanced")
    
    frame_player = create_scrollable_frame(tabview.tab("Player"))
    
    for index, (player_id, player_name) in enumerate(data["playerNames"]["value"].items()):
        player_health = data["dictionaryOfDictionaries"]["value"]["playerHealth"][player_id]
        players.append({"id": player_id, "name": player_name, "health": player_health})
    
    for idx, player in enumerate(players):
        column = idx % 2  # Left or right column
        row = idx // 2    # Row position
        
        frame = CTkFrame(frame_player, corner_radius=6)
        frame.grid(row=row, column=column, padx=10, pady=5, sticky="w")

        image_label = CTkLabel(frame, text=player["name"], font=("Arial", 12))
        image_label.pack(anchor="w", padx=5, pady=3)
        
        health_entry = CTkEntry(frame, font=("Arial", 12), width=100, border_color='#303030', fg_color="#292929")
        health_entry.pack(anchor="w", padx=5, pady=3)
        health_entry.insert(0, player["health"])
        player_entries[player["name"]] = health_entry
    
root = CTk()
root.geometry("690x440")
root.title("R.E.P.O Save Editor")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

update_ui_from_json({})  # Placeholder call
root.mainloop()
