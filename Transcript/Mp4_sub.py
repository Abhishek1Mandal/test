import subprocess

import whisper
import os
from subprocess import call
from whisper.utils import get_writer
from deep_translator import GoogleTranslator


def video2mp3(video_file, output_ext="mp3"):
    # Convert video to audio (mp3)
    filename, _ = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"


def translate_to_en(audio, audio_file=None):
    # Load the Whisper ASR model
    model = whisper.load_model("medium")  # You need to adjust the model loading part
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


def process_video_and_return_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE):
    # Load the Whisper ASR model
    model = whisper.load_model(MODEL_SIZE)

    # Define the output file name for the downloaded video
    OutputFile = 'Video.mp4'

    # Download the video using yt-dlp
    call(
        f'yt-dlp -f "mp4" --force-overwrites --no-warnings --ignore-no-formats-error --restrict-filenames -o {OutputFile} {youtube_url}',
        shell=True)

    # Convert video to audio (mp3)
    audio_file = video2mp3(OutputFile)

    # Translate transcription to en
    result_en = translate_to_en(audio_file)

    # Make subtitles
    options = {
        "max_line_width": 12,
        "max_line_count": 1,
        "highlight_words": 12
    }
    output_writer = get_writer(SUBTITLE_TYPE, '.')
    output_writer(result_en, 'subtitles_en', options)
    subtitles_ = f'subtitles_en.{SUBTITLE_TYPE}'

    # Translate subtitles
    if TARGET_LANG_CODE != 'en' and subtitles_[:-4] != '.srt':
        try:
            translate_vtt(TARGET_LANG_CODE, subtitles_)
        except:
            print(f'Invalid TARGET_LANG_CODE: {TARGET_LANG_CODE}. Generating subtitles in English')
    else:
        print('Generating subtitles in English')

    return subtitles_


# Example usage (you can call this function from another script):
if __name__ == "__main__":
    MODEL_SIZE = 'medium'
    youtube_url = 'www.youtube.com/watch?v=g_9rPvbENUw'
    TARGET_LANG_CODE = 'de'
    SUBTITLE_TYPE = 'vtt'

    subtitles = process_video_and_return_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
    print(subtitles)
