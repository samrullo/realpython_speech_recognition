import json


def get_bot_token():
    with open("secrets/token.json", "r") as fh:
        return json.load(fh)


class Config:
    bot = get_bot_token()
    bot_name = bot["bot"]
    bot_token = bot["token"]
    counter = 0
    recognition_language = "en-US"
