import json
import os

def load_settings(file_name='settings.json'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'project_settings', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)
