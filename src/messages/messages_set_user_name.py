from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    Button,
    PostbackAction,
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
        bubble = FlexBubble(
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(
                        text=f"お名前は「{user_input} 」でよろしいですか？この名前はデータ収集され、以降変更できません。",
                        wrap=True,
                    )
                ],
            ),
            footer=FlexBox(
                layout="horizontal",
                contents=[
                    Button(
                        action=PostbackAction(
                            label="Yes",
                            data=f"action=confirm&user_input={user_input_encoded}",
                            display_text="Yes",
                        )
                    ),
                    Button(
                        action=PostbackAction(
                            label="No",
                            data="action=reject",
                            display_text="No",
                        )
                    ),
                ],
            ),
        )

        # FlexMessageの生成
        return FlexMessage(alt_text="確認", contents=bubble)
