import subprocess
import threading
import time
from config_manager import load_config

video_list = []
abort_flag = False

def set_video_list(videos):
    global video_list
    video_list = videos

def play_videos_threaded(start_index=0):
    threading.Thread(target=play_videos, args=(start_index,), daemon=True).start()

def play_videos(start_index):
    global abort_flag
    abort_flag = False
    config = load_config()

    vlc_path = config["vlc_path"]
    device_1 = config["audio_device_1"]
    device_2 = config["audio_device_2"]
    ch1 = config["audio_channel_1"]
    ch2 = config["audio_channel_2"]

    for index in range(start_index, len(video_list)):
        if abort_flag:
            return

        p1 = subprocess.Popen([
            vlc_path, "--play-and-exit", video_list[index],
            "--audio-track", str(ch1),
            "--aout=mmdevice",
            f"--mmdevice-audio-device={device_1}",
            "--no-video-title-show", "--network-caching=0", "--fullscreen"
        ])
        p2 = subprocess.Popen([
            vlc_path, "--play-and-exit", video_list[index],
            "--audio-track", str(ch2),
            "--aout=mmdevice",
            f"--mmdevice-audio-device={device_2}",
            "--no-video-title-show", "--network-caching=0"
        ])

        while p1.poll() is None or p2.poll() is None:
            if abort_flag:
                p1.terminate()
                p2.terminate()
                return
            time.sleep(0.1)

def abort_playback():
    global abort_flag
    abort_flag = True