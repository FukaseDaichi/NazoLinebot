import json
import re
import importlib

from flask import g

from src.messages.messages_normal import Message as NormalMessage
from src.messages.messages_set_user_name import Message as SetUserNameMessage


class HandleMessageService:

    def __init__(self, message_dict_path="./lib/messages.json"):
        """
        HandleMessageServiceの初期化
        :param message_dict_path: メッセージ辞書のパス
        """
        self.message_dict_path = message_dict_path
        self.__load_message_dict()

    def __load_message_dict(self):
        """
        メッセージ辞書をロードし、正規表現をコンパイル
        """
        try:
            with open(self.message_dict_path, mode="r", encoding="utf-8") as file:
                self.__messagedict = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in message dictionary: {e}")

    def generate_reply_message(self, event):

        mode = g.state.get("mode")

        ## ユーザー名設定の場合
        if mode == "set_user_name":
            return SetUserNameMessage.create_message(event)

        # メッセージ辞書一致
        for key, value in self.__messagedict.items():
            if re.compile(key).fullmatch(event.message.text):
                #  クラスパスの場合
                if type(value) is str and value.startswith("src.messages"):
                    message_module = importlib.import_module(value)
                    return message_module.Message.create_message(event, value)

                return NormalMessage.create_message(event, value)
        
        ## user_name = g.user_state_manager.get_user_name(g.user_id)
        # なかった場合
        return NormalMessage.create_message(event, "デフォルトメッセージ")
