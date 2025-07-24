from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexButton,
    PostbackAction,
    FlexCarousel,
    FlexImage,
)

from src.commonclass.game_config import GAME_DATA


class Message:
    @staticmethod
    def create_game_bubble(game):
        """1つのゲーム情報からFlexBubbleを生成"""
        return FlexBubble(
            size="micro",
            hero=FlexImage(
                url=game.get("image"),
                size="full",
                aspect_mode="cover",
                aspect_ratio="320:213",
            ),
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(
                        text=game.get("title"),
                        weight="bold",
                        size="sm",
                        wrap=True,
                    ),
                    FlexBox(
                        layout="vertical",
                        contents=[
                            FlexBox(
                                layout="baseline",
                                spacing="sm",
                                contents=[
                                    FlexText(
                                        text=game.get("description"),
                                        wrap=True,
                                        color="#8c8c8c",
                                        size="xs",
                                        flex=5,
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                spacing="sm",
                padding_all="13px",
            ),
            footer=FlexBox(
                layout="vertical",
                contents=[
                    FlexButton(
                        action=PostbackAction(
                            label="はじめる",
                            data=f"action=changemode&mode={game['id']}",
                        )
                    )
                ],
            ),
        )

    @staticmethod
    def create_message(event, obj=None):
        # isGame == True のゲームだけを選ぶ
        game_list = [game for game in GAME_DATA if game.get("isGame")]

        # FlexBubbleのリストを生成
        bubbles = [Message.create_game_bubble(game) for game in game_list]

        # Carousel作成
        carousel = FlexCarousel(contents=bubbles)

        # FlexMessageを返す
        return FlexMessage(alt_text="脱出ゲーム一覧", contents=carousel)
