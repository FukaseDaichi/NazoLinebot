from functools import partial
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, args=None):
        """
        args[0]はtitleとする。
        args[1]はmessageとする。
        """
        # 値を束縛した新しい関数を作成
        target = partial(g.gas_manager.end_game, args[0], g.user_id)
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target)
        thread.start()
        
        return NormalMessage.create_message(
            event,
            args[1],
        )
