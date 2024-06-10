import json
import os
import threading

HOSTNAME = "localhost"
PORT = 1883

lock = threading.Lock()

def load_settings():
    file_path = "settings.json"
    with open(file_path, 'r') as f:
        return json.load(f)


lock = threading.Lock()



