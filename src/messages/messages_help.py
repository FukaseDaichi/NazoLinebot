from linebot.models import TextSendMessage


class Message:
    @staticmethod
    def create_message(event, __obj=None):
        return TextSendMessage(text=event.message.text)
