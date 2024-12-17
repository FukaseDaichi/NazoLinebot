from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
)
from urllib.parse import quote


class Message:
    @staticmethod
    def create_message(event, obj=None):
        user_input = event.message.text
        if len(user_input) >= 11:
            return [TextMessage(text="長さは10文字以下で入力してください。")]

        # 入力値をエンコード
        user_input_encoded = quote(user_input)

        # FlexBubbleの生成
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"「{user_input}」でよろしいですか？お名前は変更できません。",
                        "wrap": True,
                    }
                ],
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "none",
                "flex": 0,
                "contents": [
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "はい",
                            "data": f"action=confirm&user_input={user_input_encoded}",
                        },
                    },
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "いいえ",
                            "data": "action=reject",
                        },
                    },
                ],
            },
        }

        # FlexMessageの生成
        return FlexMessage(alt_text="お名前の確認", contents=bubble)
