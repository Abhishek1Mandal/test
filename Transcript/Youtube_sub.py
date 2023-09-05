import whisper
import os
import subprocess
from deep_translator import GoogleTranslator
from base64 import b64encode
from IPython.display import Audio
from whisper.utils import get_writer
from subprocess import call
from IPython.display import Audio


def video2mp3(video_file, output_ext="mp3"):
    # convert to mp3
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"


def translate_to_en(audio, audio_file=None):
    model = whisper.load_model("medium")  # Adjust the model loading part
    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audio_file, **translate_options)
    return result


def translate_vtt(target, file_subs):
    translator: GoogleTranslator = GoogleTranslator(source='auto', target=target)

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


def process_youtube_subtitles(youtube_url, TARGET_LANG_CODE, SUBTITLE_TYPE):
    MODEL_SIZE = 'medium'  # Change to the desired model size

    model = whisper.load_model(MODEL_SIZE)

    OutputFile = 'Video.mp4'
    call(
        f'yt-dlp -f "mp4" --force-overwrites --no-warnings --ignore-no-formats-error --restrict-filenames -o {OutputFile} {youtube_url}',
        shell=True)

    # Audio file
    audio_file = video2mp3(OutputFile)
    Audio(audio_file, rate=44100)

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
            print(
                f'Invalid TARGET_LANG_CODE: {TARGET_LANG_CODE}. or use subtitle type vtt. Generating subtitles in English')
    else:
        print('Generating subtitles in English')

    return subtitles_
