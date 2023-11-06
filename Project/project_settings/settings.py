import json


def load_settings(filePath='project_settings/settings.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
