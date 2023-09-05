import os
import subprocess


def video2mp3(video_file, output_ext="mp3"):
    # Convert video to audio (mp3)
    filename, _ = os.path.splitext(video_file)
    audio_file = f"{filename}.{output_ext}"
    subprocess.call(["ffmpeg", "-y", "-i", video_file, audio_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return audio_file


def process_video_to_audio(video_path):
    # Convert the video to audio (mp3)
    audio_path = video2mp3(video_path)
    return audio_path
