from flask import g
from linebot.v3.messaging import ImagemapMessage


class Message:
    @staticmethod
    def create_message(__event, obj):
        # ImagemapMessage のコンストラクタに必要となる引数を設定
        """
        obj = {
            "baseUrl": "https://example.com/image.png",
            "altText": "画像の説明",
            "baseSize": {"width": 100, "height": 100},
            "actions": [
                {"type": "postback", "label": "詳細", "data": "some_data"}
            ]
        }
        """
        message = ImagemapMessage(
            type="imagemap",  # 必須。メッセージタイプを指定
            baseUrl=obj.get("baseUrl"),  # baseUrl を設定
            altText=obj.get("altText"),  # altText を設定
            baseSize=obj.get("baseSize"),  # baseSize を設定
            actions=obj.get("actions"),  # actions を設定
        )
        return [message]
