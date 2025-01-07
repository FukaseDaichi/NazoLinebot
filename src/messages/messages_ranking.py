from flask import g
from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexSeparator,
)
import json


class Message:

    # クラス変数としてconfigをキャッシュ
    _config_cache = None

    @staticmethod
    def _load_config():
        if Message._config_cache is None:
            with open("lib/config.json", "r", encoding="utf-8") as f:
                Message._config_cache = json.load(f)
        return Message._config_cache

    @staticmethod
    def create_message(event, args=None):
        """
        args[0]はtitleとする。
        """
        results = g.gas_manager.get_score(args[0])

        # キャッシュされたconfigからtitleを取得する
        config = Message._load_config()
        title = config["title"].get(args[0], "デフォルト")

        records_top5 = []
        for score in results:
            print(f"ユーザー名: {score['userName']}, スコア: {score['score']}")
            flex_box = FlexBox(
                layout="horizontal",
                contents=[
                    FlexText(
                        text=score["userName"],
                        size="sm",
                        color="#555555",
                        flex=0,
                    ),
                    FlexText(
                        text=score["score"],
                        size="sm",
                        color="#111111",
                        align="end",
                    ),
                ],
            )
            records_top5.append(flex_box)

        bubble = FlexBubble(
            body=FlexBox(
                layout="vertical",
                contents=[
                    # 1行目: TOP5
                    FlexText(
                        text="TOP5",
                        weight="bold",
                        color="#1DB446",
                        size="sm",
                    ),
                    # 2行目: タイトル
                    FlexText(
                        text=title,
                        weight="bold",
                        size="xxl",
                        margin="md",
                    ),
                    # セパレータ
                    FlexSeparator(margin="xxl"),
                    # 名前・記録の見出し
                    FlexBox(
                        layout="horizontal",
                        margin="md",
                        contents=[
                            FlexText(text="名前", size="xs", color="#aaaaaa", flex=0),
                            FlexText(
                                text="記録", size="xs", color="#aaaaaa", align="end"
                            ),
                        ],
                    ),
                    # TOP5の実際のリスト部分
                    FlexBox(
                        layout="vertical",
                        margin="xxl",
                        spacing="sm",
                        contents=records_top5,
                    ),
                ],
            ),
        )

        # FlexMessageとして返す
        return FlexMessage(alt_text="TOP5ランキング", contents=bubble)
