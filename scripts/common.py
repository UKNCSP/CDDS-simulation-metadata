from pathlib import Path
import json
import sys


def read_json(source_path: Path):
    """Opens a single json file and returns the contents as a dictionary.

    Parameters
    ----------
    source_path: Path
        The path to the source JSON file.

    Returns
    -------
    dict
        The JSON file contents as a dictionary.
    """
    try:
        with open(source_path, 'r') as f:
            dictionary = json.load(f)
    except FileNotFoundError:
        print(f"{source_path} does not exist. Please check the file path that you have provided.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"This json file is invalid: {e}")
        sys.exit()

    return dictionary
