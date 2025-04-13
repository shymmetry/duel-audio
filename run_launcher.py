import tkinter as tk
from tkinter import messagebox, filedialog
import os
import threading
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config_manager import load_config, config_exists, save_config
from vlc_launcher import play_videos_threaded, abort_playback, set_video_list
from config_gui import open_config_window

video_files = []

def select_folder():
    global video_files
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        video_files = [
            os.path.normpath(os.path.join(folder_selected, f))
            for f in sorted(os.listdir(folder_selected))
            if f.endswith(('.mp4', '.avi', '.mkv'))
        ]
        set_video_list(video_files)
        if video_files:
            launch_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "No valid video files found.")

def launch_selected_video():
    if not video_files:
        messagebox.showerror("Error", "No videos loaded.")
        return

    selected = filedialog.askopenfilename(
        initialdir=os.path.dirname(video_files[0]),
        filetypes=[("Video files", "*.mp4 *.avi *.mkv")]
    )

    if selected:
        selected = os.path.normcase(os.path.normpath(selected))
        normalized_files = [os.path.normcase(os.path.normpath(f)) for f in video_files]

        if selected in normalized_files:
            start_index = normalized_files.index(selected)
            play_videos_threaded(start_index)
        else:
            messagebox.showerror("Error", "Selected file is not in the loaded folder.")

def confirm_abort():
    abort_playback()
    root.quit()

def open_config():
    open_config_window(root)

root = tk.Tk()
root.title("Dual VLC Playlist Player")

tk.Label(root, text="Select a folder with videos to play:").pack(pady=10)

tk.Button(root, text="Select Folder", command=select_folder).pack(pady=5)
launch_button = tk.Button(root, text="Launch Videos", command=launch_selected_video, state=tk.DISABLED)
launch_button.pack(pady=5)
tk.Button(root, text="Configure Audio", command=open_config).pack(pady=5)
tk.Button(root, text="Abort Playback", command=confirm_abort).pack(pady=5)

root.mainloop()