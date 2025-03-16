# <img src="./icon.ico" alt="Icon" width="30" style="vertical-align: middle;"> R.E.P.O Save Editor


## Overview

**R.E.P.O Save Editor** is a Python-based graphical user interface (GUI) tool designed to edit and manage save files for a game called **R.E.P.O**. The tool allows users to modify various game statistics such as currency, player health, and other in-game data. It also enables exporting the data in ES3 format.

This tool is built using `CustomTkinter`, `Pillow`, and other libraries, providing a clean and user-friendly interface for the editing process. It supports Steam profile integration, allowing players' profile pictures to be fetched and displayed.

## Features

- **Decrypt and Load `.es3` Save Files**: Open `.es3` files and decrypt them for editing.
- **Edit Game Data**: View and modify player stats, world stats, and more in a user-friendly interface.
- **JSON-Based Editing**: Convert decrypted `.es3` data to JSON for easy editing and saving.
- **Re-Encrypt and Save**: Save the edited data back into `.es3` format after re-encrypting it.


## How to Use  

1. **Download the latest release**:  
   Go to the [Releases page](https://github.com/yourusername/R.E.P.O-Save-Editor/releases) and download the latest version of the tool.  

2. **Open the save files folder**:  
   Click on the "File" button, then choose "Open Save". The tool will automatically open in the save files directory. Select the folder of the save you want to edit, then choose the `.es3` file (not the backup version) to load. The tool will decrypt and load the data into a JSON format for editing.  

3. **Edit the Data**:  
   Modify values such as player health, currency, or any other editable fields in the game data.  

4. **Save Changes**:  
   After making your edits, click "Save" to apply the changes directly to the `.es3` file. The modified JSON data is re-encrypted and saved back in the same format.

## Contributions

Feel free to fork the repository and submit pull requests for any improvements or bug fixes!

---


### For Developers

Make sure you have Python 3.8 or newer installed. You can download Python from [here](https://www.python.org/downloads/).

To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
