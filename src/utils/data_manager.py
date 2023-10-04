from pathlib import Path
import pickle
import tkinter as tk
from tkinter.filedialog import askopenfilename
from config.directories import USER_GAME_DIR

class DataManager:
    def __init__(self) -> None:
        self.SAVE_FOLDER = USER_GAME_DIR
        self.SAVE_FOLDER.mkdir(parents=True, exist_ok=True)
        self.FILENAME = "placeholder.pkl"
        self.data = {
            "GAME_DATA" : {
                "map" : "test"
            },
            "PLAYER_DATA" : None,
            "QUEST_DATA" : None
        }

    def set_filename(self, new_name: str):
        if new_name.split(".")[-1].upper() == "PKL":
            self.FILENAME = new_name
        else: print("INVALID FILENAME, MUST END IN .PKL")
    
    def set_player_data(self, player):
        self.data["PLAYER_DATA"] = player

    def save_game_data(self):
        file_path = self.SAVE_FOLDER / self.FILENAME
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(self.data, file)
            print(f"Game data saved to {file_path}")
        except Exception as e:
            print(f"Error saving game data: {str(e)}")

    def load_game_data(self, filename):
        file_path = self.SAVE_FOLDER / filename
        try:
            with open(file_path, 'rb') as file:
                load_data = pickle.load(file)
            self.FILENAME = filename
            self.data = load_data
            print(f"Data loaded from {file_path}")
            return load_data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"Error loading game data: {str(e)}")
            return None
    
    def select_file(self):
        tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
        path = askopenfilename(
            defaultextension = ".pkl",
            initialdir = self.SAVE_FOLDER
        )
        return path
    
    def load_game(self):
        path = self.select_file()
        file = path.split("/")[-1]
        self.load_game_data(file)

    def create_new_game(self, player):
        self.set_player_data(player)
        name = player.name
        filename = f"{name}.pkl"
        i = 1
        while Path.exists(self.SAVE_FOLDER / filename):
            filename = f"{name}_{i}.pkl"
            i += 1
        self.FILENAME = filename
        self.save_game_data()
