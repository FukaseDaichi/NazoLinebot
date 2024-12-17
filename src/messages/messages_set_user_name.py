from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexButton,
    PostbackAction,
)
from urllib.parse import quote

MAX_LENGTH = 10

class Message:
    @staticmethod
    def create_message(event, obj=None):
        user_input = event.message.text
        if len(user_input) >= 11:
            return TextMessage(text=f"長さは{MAX_LENGTH}文字以下で入力してください。")

        # 入力値をエンコード
        user_input_encoded = quote(user_input)

        # FlexMessageのBubbleを定義
        # FlexMessageのBubble構造を定義
        bubble = FlexBubble(
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(
                        text=f"「{user_input}」でよろしいですか？お名前は変更できません。",
                        wrap=True,
                    )
                ],
            ),
            footer=FlexBox(
                layout="horizontal",
                spacing="none",
                flex=0,
                contents=[
                    FlexButton(
                        height="sm",
                        action=PostbackAction(
                            label="はい",
                            data=f"action=register&user_input={user_input_encoded}",
                        ),
                    ),
                    FlexButton(
                        height="sm",
                        action=PostbackAction(label="いいえ", data="action=reject"),
                    ),
                ],
            ),
        )

        # FlexMessageを生成
        return FlexMessage(alt_text="お名前の確認", contents=bubble)
