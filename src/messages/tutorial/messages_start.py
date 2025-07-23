from functools import partial
from flask import g
from src.messages.messages_image import Message as ImgMessage
import threading


class Message:
    @staticmethod
    def create_message(event, __args):
        # 値を束縛した新しい関数を作成
        target = partial(g.firebase_manager.start_game, "tutorial", g.user_id)
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target)
        thread.start()
        return ImgMessage.create_message(
            event, "https://nazolinebot.onrender.com/resources/img/tutorial.png"
        )
