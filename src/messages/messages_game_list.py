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


class Message:
    @staticmethod
    def create_message(event, obj=None):
        # FlexMessageのCarouselを定義
        tutorial = FlexBubble(
            size="micro",
            hero=FlexImage(
                url="https://developers-resource.landpress.line.me/fx/clip/clip10.jpg",
                size="full",
                aspect_mode="cover",
                aspect_ratio="320:213",
            ),
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(
                        text="チュートリアル", weight="bold", size="sm", wrap=True
                    ),
                    FlexBox(
                        layout="vertical",
                        contents=[
                            FlexBox(
                                layout="baseline",
                                spacing="sm",
                                contents=[
                                    FlexText(
                                        text="チュートリアル用の脱出ゲーム。1分～",
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
                            label="はじめる", data="action=changemode&mode=tutorial"
                        )
                    )
                ],
            ),
        )

        first = FlexBubble(
            size="micro",
            hero=FlexImage(
                url="https://developers-resource.landpress.line.me/fx/clip/clip10.jpg",
                size="full",
                aspect_mode="cover",
                aspect_ratio="320:213",
            ),
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(text="FIRST", weight="bold", size="sm", wrap=True),
                    FlexBox(
                        layout="vertical",
                        contents=[
                            FlexBox(
                                layout="baseline",
                                spacing="sm",
                                contents=[
                                    FlexText(
                                        text="最初の脱出ゲーム",
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
                            label="はじめる", data="action=changemode&mode=first"
                        )
                    )
                ],
            ),
        )

        carousel = FlexCarousel(contents=[tutorial,first])

        # FlexMessageを生成
        return FlexMessage(alt_text="脱出ゲーム一覧", contents=carousel)
