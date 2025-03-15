# <img src="./icon.ico" alt="Icon" width="30" style="vertical-align: middle;"> R.E.P.O Save Editor


## Overview

**R.E.P.O Save Editor** is a Python-based graphical user interface (GUI) tool designed to edit and manage save files for a game called **R.E.P.O**. The tool allows users to modify various game statistics such as currency, player health, and other in-game data. It also enables exporting the data in JSON format for easy backup and sharing.

This tool is built using `CustomTkinter`, `Pillow`, and other libraries, providing a clean and user-friendly interface for the editing process. It supports Steam profile integration, allowing players' profile pictures to be fetched and displayed.

## Features

- **Edit Game Save Data**: Modify values like currency, lives, player health, and more.
- **Profile Picture Integration**: Fetch Steam profile pictures based on player ID and display them in the editor.
- **JSON Editing**: Advanced tab for editing the raw JSON data with syntax highlighting for ease of use.
- **Save & Load**: Load existing save data and save changes to a file.
- **Profile Picture Caching**: Profile pictures are cached locally to improve efficiency.

## Installation

### For Developers

Make sure you have Python 3.6 or later installed. You can download Python from [here](https://www.python.org/downloads/).

To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
