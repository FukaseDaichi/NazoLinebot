import json
import re
import importlib

from src.messages.messages_normal import Message as NormalMessage


class HandleMessageService:

    # メッセージ辞書
    __messagedict = json.load(
        open(file="./lib/messagedict.json", mode="r", encoding="utf-8")
    )

    @staticmethod
    def generate_reply_message(event):

        # メッセージ辞書一致
        for key in HandleMessageService.__messagedict:
            if re.compile(key).fullmatch(event.message.text):
                matchData = HandleMessageService.__messagedict[key]
                
                #  クラスパスの場合
                if type(matchData) is str and matchData.startswith("src.messages"):
                    message_module = importlib.import_module(matchData)
                    return message_module.Message.create_message(event)

                return NormalMessage.create_message(
                    event, HandleMessageService.__messagedict[key]
                )

        # なかった場合
        return NormalMessage.create_message(event, "デフォルトメッセージ")
