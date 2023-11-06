import json


def load_settings(filePath='/Users/bane/Documents/GitHub/IoT-projekat/Project/project_settings/settings.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
