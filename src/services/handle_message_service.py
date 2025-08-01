import json
import re
import importlib

from flask import g

from src.messages.messages_normal import Message as NormalMessage
from src.messages.messages_set_user_name import Message as SetUserNameMessage


class HandleMessageService:

    def __init__(self, config_path="./lib/config.json"):
        """
        HandleMessageServiceの初期化
        :param message_dict_path: メッセージ辞書のパス
        """
        self.config_path = config_path
        self.__load_config()
        self.__load_message_dicts()

    def __load_config(self):
        """
        設定ファイルをロード
        """
        try:
            with open(self.config_path, mode="r", encoding="utf-8") as file:
                self.config = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {e}")

    def __load_message_dicts(self):
        """
        config["games"]配列のidをdict_name、pathをファイルパスとして辞書を読み込む
        """
        self.__messagedicts = {}
        for game in self.config.get("games", []):
            dict_name = game.get("id")
            dict_path = game.get("path")
            if dict_name and dict_path:
                try:
                    with open(dict_path, mode="r", encoding="utf-8") as file:
                        self.__messagedicts[dict_name] = json.load(file)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Invalid JSON format in message dictionary {dict_name}: {e}"
                    )
                except FileNotFoundError as e:
                    raise ValueError(
                        f"Message dictionary file not found for {dict_name}: {e}"
                    )

    def generate_reply_message(self, event):

        mode = g.state.get("mode")

        ## ユーザー名設定の場合
        if mode == "set_user_name":
            return SetUserNameMessage.create_message(event)

        # メッセージ辞書一致
        message_dict = self.__messagedicts[mode]
        for key, value in message_dict.items():
            if re.compile(key, re.IGNORECASE).fullmatch(event.message.text):
                #  クラスパスの場合
                if type(value) is str and value.startswith("src.messages"):
                    params = value.split("||")
                    message_module = importlib.import_module(params[0])

                    param = params[1:] if len(params) > 1 else None
                    return message_module.Message.create_message(event, param)

                return NormalMessage.create_message(event, value)

        ## user_name = g.user_state_manager.get_user_name(g.user_id)
        # なかった場合
        return NormalMessage.create_message(event, "デフォルトメッセージ")
