import json
import os
import threading

# HOSTNAME = "10.1.121.63"
HOSTNAME = "localhost"

PORT = 1883

lock = threading.Lock()

def load_settings():
    file_path = "settings/settings.json"
    with open(file_path, 'r') as f:
        return json.load(f)


lock = threading.Lock()



