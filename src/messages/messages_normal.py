from linebot.models import TextSendMessage

class Message:
    @staticmethod
    def create_message(__event, obj=None):

        # リストじゃない場合
        if type(obj) != list:
            return TextSendMessage(text=obj)

        messages = []
        for key in obj:
            messages.append(TextSendMessage(text=key))

        return messages
