import whisper
from subprocess import call


def process_youtube_video(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE):
    # Load the Whisper ASR model
    model = whisper.load_model(MODEL_SIZE)

    # Define the output file name for the downloaded video
    OutputFile = 'Video.mp4'

    # Download the video using yt-dlp
    call(
        f'yt-dlp -f "mp4" --force-overwrites --no-warnings --ignore-no-formats-error --restrict-filenames -o {OutputFile} {youtube_url}',
        shell=True)

    # Process the downloaded video further
    # ... Add your code for additional processing here ...

    return "Video processing complete."


# Example usage (you can call this function from another script):
if __name__ == "__main__":
    MODEL_SIZE = 'medium'
    youtube_url = 'www.youtube.com/watch?v=g_9rPvbENUw'
    TARGET_LANG_CODE = 'de'
    SUBTITLE_TYPE = 'vtt'

    process_youtube_video(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
