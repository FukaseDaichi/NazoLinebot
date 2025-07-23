from functools import partial
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, args=None):

        user_message = event.message.text

        if user_message == g.state.get("user_name"):
            # 正解時

            # 記録追加
            target = partial(g.firebase_manager.end_game, "tutorial", g.user_id)
            # スレッドを作成して非同期で実行
            thread = threading.Thread(target=target)
            thread.start()

            return NormalMessage.create_message(
                event,
                [
                    "正解！！ おめでとう！！\r\n「スコア」と入力するとあなたのスコアがわかります。「ランキング」でtop5がわかります。",
                    "チュートリアルは以上です。「一覧」と入力すると他の謎が解けます。",
                ],
            )

        return NormalMessage.create_message(
            event,
            "「一覧」と入力すると他のゲームが遊べます。",
        )
