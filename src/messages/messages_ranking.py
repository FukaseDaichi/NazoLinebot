from functools import partial
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, args=None):
        """
        args[0]はtitleとする。
        """
        results = g.gas_manager.get_score(args[0])

        for score in results:
            print(f"ユーザー名: {score['userName']}, スコア: {score['score']}")
