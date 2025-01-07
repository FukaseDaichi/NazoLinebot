from flask import g
from linebot.v3.messaging import ImageMessage


class Message:
    @staticmethod
    def create_message(__event, obj=None):

        # リストじゃない場合
        if type(obj) != list:
            return [ImageMessage(original_content_url=obj, preview_image_url=obj)]

        messages = []
        for key in obj:
            messages.append(
                ImageMessage(original_content_url=key, preview_image_url=key)
            )

        return messages
