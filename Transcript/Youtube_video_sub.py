from Common.Common import video2mp3, translate_vtt, translate_to_en
import os
from base64 import b64encode
from fastapi import UploadFile, Form
from tempfile import NamedTemporaryFile
import whisper

# Initialize your whisper model
MODEL_SIZE = 'medium'
model = whisper.load_model(MODEL_SIZE)


def process_video(video_path: str, target_lang_code: str, subtitle_type: str):
    # Convert video to mp3
    mp3_file = video2mp3(video_path)

    # Translate audio to English
    translated_text = translate_to_en(mp3_file)

    # Translate subtitles to target language
    translated_subtitles_path = "subtitles_en.vtt"
    translate_vtt(target_lang_code, translated_subtitles_path)

    return {
        "translated_text": translated_text,
        "translated_subtitles": translated_subtitles_path
    }


if __name__ == "__main__":
    # Example usage
    video_path = "example.mp4"  # Provide the actual video file path
    target_lang_code = "de"
    subtitle_type = "vtt"

    response = process_video(video_path, target_lang_code, subtitle_type)
    print(response)
