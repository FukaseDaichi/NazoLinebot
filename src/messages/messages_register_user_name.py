from urllib.parse import unquote
from flask import g
from src.messages.messages_normal import Message as NormalMessage


class Message:
    @staticmethod
    def create_message(event, obj=None):
        data =event.postback.data
        params = dict(x.split("=") for x in data.split("&"))
        user_input = params.get("user_input")

        ## URLデコードを行う
        user_input = unquote(user_input)

        g.register_user(g.user_id, user_input)

        return NormalMessage.create_message(event,f"{user_input}で登録しました。")
