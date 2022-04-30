from ast import Call
import os
from click import Context
from config import Config
import logging
from telegram.ext import Updater
from telegram import Update, File
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
import speech_recognition as sr
from recognizer import recognize_voice_message

from set_language_command_handlers import add_lg_setter_handlers_to_dispatcher, initialize_recognition_language, add_choose_language_handler

recognizer = sr.Recognizer()
initialize_recognition_language()

# updater will be used to get updates, i.e. any kind of message sent to the bot
updater = Updater(token=Config.bot_token, use_context=True)

# dispatcher will be used to dispatch various handlers such as CommandHandler, MessageHandler or ConversationHandler
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""I am a speech recognition bot. I will try to recognize speech from recorded audio using Google Speech Recognition API via SpeechRecognition python library!\n
                To choose recognition language:\n
                /choose_language""",
    )


def stop(update: Update, context: CallbackContext):
    logging.info(f"will stop the bot {Config.bot_name}")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Bye, bye, I will stop myself now..."
    )
    updater.stop()


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler("stop", stop)
dispatcher.add_handler(stop_handler)

# Add command handler to choose the language for speech recognition
add_choose_language_handler(dispatcher)

# Displays Commands to change speech recognition language
add_lg_setter_handlers_to_dispatcher(dispatcher)

# The MessageHandler that expects voice message for speech recognition
message_handler = MessageHandler(
    filters=None, callback=lambda update, context: recognize_voice_message(update, context, recognizer))
dispatcher.add_handler(message_handler)

# start polling chat with the bot
updater.start_polling()
