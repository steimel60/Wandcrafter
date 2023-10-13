from pathlib import Path
import pickle
import tkinter as tk
from tkinter.filedialog import askopenfilename
from config.directories import USER_GAME_DIR

def save_game_data(file_path : Path, data):
    """
    Save game data to a specified file using pickle serialization.

    Args:
        file_path (Path): The path to the file where the game data will be saved.
        data: The data to be saved.

    Raises:
        Exception: If an error occurs during the save process.
    """
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f"Game data saved to {file_path}")
    except (IOError, pickle.PickleError) as e:
        if isinstance(e, IOError):
            print(f"IO error: {e}")
        elif isinstance(e, pickle.PickleError):
            print(f"Pickle error:, {e}")

def load_game_data(file_path: Path):
    """
    Load game data from a specified file using pickle deserialization.

    Args:
        file_path (Path): The path to the file from which the game data will be loaded.

    Returns:
        Loaded game data if successful, None on error or file not found.

    """
    try:
        with open(file_path, 'rb') as file:
            load_data = pickle.load(file)
        print(f"Data loaded from {file_path}")
        return load_data
    except (FileNotFoundError, IOError, pickle.PickleError) as e:
        if isinstance(e, FileNotFoundError):
            print(f"File not found: {file_path}")
        elif isinstance(e, IOError):
            print(f"IO error: {e}")
        elif isinstance(e, pickle.PickleError):
            print(f"Pickle error:, {e}")
        return None

def select_file() -> Path:
    """
    Open a file dialog for selecting a file.

    Returns:
        The selected file's path or None if the user cancels or
        if the returned path is not a file.
    """
    tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions
    path = askopenfilename(
        defaultextension=".pkl",
        initialdir=USER_GAME_DIR
    )
    path = Path(path)
    if path.is_file():
        return path
    print("Invalid file path.")
    return None

def select_saved_game():
    """Opens file explorer then opens a saved game."""
    path = select_file()
    if path is not None:
        return load_game_data(path)
    return None
