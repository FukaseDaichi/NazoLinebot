import json
from linebot.v3.messaging import (
    TextMessage,
)
import re
import importlib
from src.messages.messages_normal import Message as NormalMessage


class HandlePostbackService:

    def __init__(self, message_dict_path="./lib/postbacks.json"):
        """
        HandleMessageServiceの初期化
        :param message_dict_path: メッセージ辞書のパス
        """
        self.message_dict_path = message_dict_path
        self.__load_message_dict()

    def __load_message_dict(self):
        """
        メッセージ辞書をロード
        """
        try:
            with open(self.message_dict_path, mode="r", encoding="utf-8") as file:
                raw_dict = json.load(file)
            self.__postbacks = {re.compile(key): value for key, value in raw_dict.items()}
        except Exception as e:
            raise ValueError(f"Failed to load message dictionary: {e}")

    def generate_reply_message(self, event):
        # クラスリスト一致検索
        for regex, value in self.__postbacks:
            if regex.fullmatch(event.postback.data):

                ## クラスの場合
                if type(value) is str and value.startswith("src.messages"):
                    message_module = importlib.import_module(value)
                    return message_module.Message.create_message(event, value)
                
                return NormalMessage.create_message(event, value)

        # なかった場合
        return NormalMessage.create_message(event, "例外が発生しました")
