from pathlib import Path
import json

def import_json_file(json_path):

    # Define the path using pathlib for cross-platform compatibility
    file_path = Path(json_path)

    # Open and load the JSON content
    with file_path.open(encoding='utf-8') as f:
        json_object = json.load(f)

    return json_object