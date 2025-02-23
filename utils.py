import json 
import json
import re

def read_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fix_and_load_json(input_path):
    """
    Fixes JSON formatting issues and returns the parsed dictionary.

    Args:
        input_path (str): Path to the original JSON file.

    Returns:
        dict: Parsed JSON data if successful, otherwise None.
    """
    try:
        # Read the file as raw text
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Escape newlines and ensure proper string closing
        content = re.sub(r'(?<!\\)\n', '\\n', content)  # Fix unescaped newlines
        content = re.sub(r'(".*?)(?<!\\)"\s*,?\s*\n', r'\1"', content)  # Ensure closing quotes

        # Parse the fixed JSON content
        data = json.loads(content)
        return data

    except json.JSONDecodeError as e:
        print(f"❌ JSONDecodeError: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
