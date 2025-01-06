from functools import partial
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, obj=None):
        # 値を束縛した新しい関数を作成
        target = partial(g.gas_manager.start_game, "tutorial", g.user_id)
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target)
        thread.start()

        return NormalMessage.create_message(event, "開始しました。")
