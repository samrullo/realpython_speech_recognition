import os
from telegram import Update
from telegram.ext import CallbackContext
import pathlib
import subprocess
import logging
from speech_recognition import Recognizer
import datetime
from datetime_utils import get_date_and_time_as_string
from sr_utils import recognize_speech_from_audio_file
from config import Config


def recognize_voice_message(update: Update, context: CallbackContext, recognizer: Recognizer, show_file_info=False):
    if update.message.voice:
        # if it is a voice message we access it
        voice_message = update.message.voice

        # we want to download voice message as a file
        voice_file = voice_message.get_file()
        download_folder = pathlib.Path(
            "download") / f"chat_id_{update.message.chat_id}"
        if not download_folder.exists():
            os.makedirs(download_folder)
        filename = (
            f"voice_message_{get_date_and_time_as_string(datetime.datetime.now())}.ogg"
        )
        download_filepath = (download_folder) / filename
        wav_filepath = download_folder / f"{download_filepath.stem}.wav"

        # update.message.voice.get_file() returns File object that has download method
        downloaded_file = voice_file.download(f"{download_folder}/{filename}")

        # now we will convert ogg file into wav file
        subprocess.run(
            ["ffmpeg", "-i", str(download_filepath), str(wav_filepath)])

        # assuming conversion to wav file was successfull let's try to recognize it
        if wav_filepath.exists():
            logging.info(
                f"{wav_filepath} seemed to happen successfully, will proceed to recognizing it"
            )
            response = recognize_speech_from_audio_file(
                recognizer, str(wav_filepath), lang=Config.recognition_language
            )
        else:
            response = {"transcription": f"{wav_filepath} doesn't exist"}

        _text = response["transcription"]
        if show_file_info:
            _text = f"""You sent voice message\n
                    File_id : {voice_message.file_id}\n
                    File size : {voice_message.file_size}\n
                    Voice message duration : {voice_message.duration} seconds\n
                    Downloaded file : {downloaded_file}\n
                    Recognition result : {response['transcription']}"""

    elif not update.message.text:
        _text = "You sent no text dear"
    else:
        _text = update.message.text
    logging.info(update.message)
    update.message.reply_text(_text)
