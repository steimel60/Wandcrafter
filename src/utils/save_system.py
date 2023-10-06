from pathlib import Path
import pickle
import tkinter as tk
from tkinter.filedialog import askopenfilename
from config.directories import USER_GAME_DIR

def save_game_data(file_path, data):
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f"Game data saved to {file_path}")
    except Exception as e:
        print(f"Error saving game data: {str(e)}")

def load_game_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            load_data = pickle.load(file)
        print(f"Data loaded from {file_path}")
        return load_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading game data: {str(e)}")
        return None

def select_file():
    tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
    path = askopenfilename(
        defaultextension = ".pkl",
        initialdir = USER_GAME_DIR
    )
    return path

def select_saved_game():
    path = select_file()
    file = Path(path).name
    return load_game_data(path)
