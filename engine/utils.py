import json


def json_to_dict(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File '{json_file}' Not Found")
        return None
    except json.decoder.JSONDecodeError:
        print(f"Unable to extract JSON from '{json_file}'")
        return None