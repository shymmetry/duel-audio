import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

default_config = {
    "vlc_path": "C:/Program Files/VideoLAN/VLC/vlc.exe",
    "audio_device_1": "default1",
    "audio_device_2": "default2",
    "audio_channel_1": 1,
    "audio_channel_2": 0
}

def config_exists():
    return os.path.exists(CONFIG_PATH)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return default_config
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)