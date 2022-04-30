from telegram.ext import CommandHandler, CallbackContext, Updater
from telegram import Update
from config import Config

supported_languages = {
    "english": "en-US",
    "russian": "ru-RU",
    "uzbek": "uz-UZ",
    "japanese": "ja-JP",
}


def initialize_recognition_language():
    Config.recognition_language = supported_languages["english"]


def set_recognition_language(update: Update, context: CallbackContext, language=None):
    Config.recognition_language = supported_languages[language]
    update.message.reply_text(f"Set recognition language to {language}")


lg_setting_command_handler = {
    "english": CommandHandler(
        "english",
        lambda update, context: set_recognition_language(update, context, "english"),
    ),
    "russian": CommandHandler(
        "russian",
        lambda update, context: set_recognition_language(update, context, "russian"),
    ),
    "japanese": CommandHandler(
        "japanese",
        lambda update, context: set_recognition_language(update, context, "japanese"),
    ),
    "uzbek": CommandHandler(
        "uzbek",
        lambda update, context: set_recognition_language(update, context, "uzbek"),
    ),
}


def add_lg_setter_handlers_to_dispatcher(dispather: Updater.dispatcher):
    for lg, handler in lg_setting_command_handler.items():
        dispather.add_handler(handler)


def curr_lg_marker(lg):
    return "*" if Config.recognition_language == supported_languages[lg] else ""


def lg_cmd_list():
    return "\n".join([f"/{lg} {curr_lg_marker(lg)}" for lg in supported_languages])


def choose_language(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"""Choose recognition language:\n{lg_cmd_list()}"""
    )


choose_language_handler = CommandHandler("choose_language", choose_language)


def add_choose_language_handler(dispatcher: Updater.dispatcher):
    dispatcher.add_handler(choose_language_handler)
