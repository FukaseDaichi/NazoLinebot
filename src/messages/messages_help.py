from linebot.v3.messaging import (
    TextMessage,
)


class Message:
    @staticmethod
    def create_message(event, __obj=None):
        return [TextMessage(text=event.message.text)]
