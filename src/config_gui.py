from device_finder import get_audio_devices_with_ids
import tkinter as tk
from tkinter import ttk
from config_manager import save_config, load_config

def open_config_window(parent):
    config = load_config()
    device_map = get_audio_devices_with_ids()

    friendly_names = list(device_map.keys())

    win = tk.Toplevel(parent)
    win.title("Configure Audio Devices")

    # VLC Path
    tk.Label(win, text="VLC Path:").grid(row=0, column=0, sticky="e")
    vlc_entry = tk.Entry(win, width=50)
    vlc_entry.insert(0, config["vlc_path"])
    vlc_entry.grid(row=0, column=1)

    # Audio Device 1
    tk.Label(win, text="Audio Device 1:").grid(row=1, column=0, sticky="e")
    ad1 = ttk.Combobox(win, values=friendly_names, width=47)
    ad1.set(get_key_for_value(device_map, config["audio_device_1"]))
    ad1.grid(row=1, column=1)

    # Audio Device 2
    tk.Label(win, text="Audio Device 2:").grid(row=2, column=0, sticky="e")
    ad2 = ttk.Combobox(win, values=friendly_names, width=47)
    ad2.set(get_key_for_value(device_map, config["audio_device_2"]))
    ad2.grid(row=2, column=1)

    # Audio Channels
    tk.Label(win, text="Audio Channel 1:").grid(row=3, column=0, sticky="e")
    ch1 = tk.Spinbox(win, from_=0, to=5, width=5)
    ch1.delete(0, "end")
    ch1.insert(0, config["audio_channel_1"])
    ch1.grid(row=3, column=1, sticky="w")

    tk.Label(win, text="Audio Channel 2:").grid(row=4, column=0, sticky="e")
    ch2 = tk.Spinbox(win, from_=0, to=5, width=5)
    ch2.delete(0, "end")
    ch2.insert(0, config["audio_channel_2"])
    ch2.grid(row=4, column=1, sticky="w")

    def save():
        new_config = {
            "vlc_path": vlc_entry.get(),
            "audio_device_1": device_map.get(ad1.get(), ""),
            "audio_device_2": device_map.get(ad2.get(), ""),
            "audio_channel_1": int(ch1.get()),
            "audio_channel_2": int(ch2.get())
        }
        save_config(new_config)
        win.destroy()

    tk.Button(win, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=10)

def get_key_for_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return ""