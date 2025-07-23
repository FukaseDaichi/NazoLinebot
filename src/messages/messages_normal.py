from flask import g
from linebot.v3.messaging import (
    TextMessage,
)


class Message:
    @staticmethod
    def create_message(__event, obj=None):

        def replace_user_name(text):
            if "{user_name}" in text:
                user_name = g.user_state_manager.get_user_name(g.user_id)
                return text.replace("{user_name}", user_name)
            return text

        # リストじゃない場合
        if type(obj) != list:
            obj = replace_user_name(obj)
            return [TextMessage(text=obj)]

        messages = []
        for key in obj:
            key = replace_user_name(key)
            messages.append(TextMessage(text=key))

        return messages
