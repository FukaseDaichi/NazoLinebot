from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    PostbackAction,
)


class Message:
    @staticmethod
    def create_message(event, obj=None):
        user_input = event.message.text
        if len(user_input) >= 11:
            return [TextMessage(text="長さは10文字以下で入力してください。")]

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
                    FlexBox(
                        layout="vertical",
                        contents=[
                            PostbackAction(
                                label="Yes",
                                data=f"action=confirm&user_input={user_input}",
                                display_text="Yes",
                            )
                        ],
                    ),
                    FlexBox(
                        layout="vertical",
                        contents=[
                            PostbackAction(
                                label="No", data="action=reject", display_text="No"
                            )
                        ],
                    ),
                ],
            ),
        )
        return [FlexMessage(alt_text="確認", contents=bubble)]
