from customtkinter import *
from tkinter import TOP, X, BOTH
from lib.CTkMenuBar import *

file = None

root  = CTk()
root.geometry("600x400")
root.title("R.E.P.O Save Editor")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")
# Font settings
font = ("Arial", 14)
# Menu
menu = CTkTitleMenu(master=root)
button_1 = menu.add_cascade("File")

dropdown1 = CustomDropdownMenu(widget=button_1)
dropdown1.add_option(option="Open", command=lambda: print("Open"))
dropdown1.add_option(option="Save", command=lambda: print("Save"))
dropdown1.add_separator()
sub_menu = dropdown1.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".JSON")

# Tabview
tabview = CTkTabview(root, width=600, height=400)
tabview.pack(fill=BOTH, expand=2)
tabview.add("World")  # add tab at the end
tabview.add("Player")  # add tab at the end
tabview.add("Advanced")  # add tab at the end

label_1 = CTkLabel(tabview.tab("World"), text="Balance: ", font=font)
label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_1 = CTkEntry(tabview.tab("World"), font=font)
entry_1.grid(row=0, column=1, padx=20, pady=5, sticky="e")

label_2 = CTkLabel(tabview.tab("World"), text="Currency: ", font=font)
label_2.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_2 = CTkEntry(tabview.tab("World"), font=font)
entry_2.grid(row=1, column=1, padx=20, pady=5, sticky="e")
root.mainloop()