import gradio as gr
import os
import subprocess
from os.path import exists as path_exists
from pathlib import Path
from whisper.utils import get_writer
from deep_translator import GoogleTranslator
from IPython.display import HTML
from base64 import b64encode
from IPython.display import Audio
import whisper


def video2mp3(video_file, output_ext="mp3"):
    # convert to mp3
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"


def translate_to_en(audio, audio_file=None):
    # en translate
    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audio_file, **translate_options)
    return result


def translate_vtt(target, file_subs):
    translator = GoogleTranslator(source='auto', target=target)

    with open(os.path.join('.', file_subs), "r+") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i % 3 == 0 and line.strip() != 'WEBVTT':
                # Translate the line
                translated_line = translator.translate(line.strip())
                # Replace
                lines[i] = translated_line + '\n'
                print(lines[i])
        file.seek(0)
        file.writelines(lines)


def encode_audio_base64(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_base64 = b64encode(audio_file.read()).decode()
    return audio_base64


model = whisper.load_model("large")  # You need to adjust the model loading part
