import json
from linebot.v3.messaging import (
    TextMessage,
)
import re
import importlib


class HandlePostbackService:

    # クラスリスト
    __postback_classList = json.load(
        open(file="./lib/postbacks.json", mode="r", encoding="utf-8")
    )

    @staticmethod
    def generate_reply_message(event):

        # クラスリスト一致検索
        for key in HandlePostbackService.__postback_classList:
            if re.compile(key).fullmatch(event.postback.data):
                message_module = importlib.import_module(
                    HandlePostbackService.__postback_classList[key]
                )
                return message_module.Message.create_message(
                    event, HandlePostbackService.__postback_classList[key]
                )

        # なかった場合
        return TextMessage(text="例外が発生しました。")
