from linebot.v3.messaging import (
    TextMessage,
)

class Message:
    @staticmethod
    def create_message(__event, obj=None):
        # リストじゃない場合
        if type(obj) != list:
            return [TextMessage(text=obj)]

        messages = []
        for key in obj:
            messages.append(TextMessage(text=key))

        return messages
