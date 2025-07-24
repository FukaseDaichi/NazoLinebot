from flask import g
from src.messages.messages_normal import Message as NormalMessage


class Message:
    @staticmethod
    def create_message(event, args=None):
        """
        args[0]はtitleとする。
        """
        # 値を束縛した新しい関数を作成
        score = g.firebase_manager.get_user_score(g.user_id, args[0])
        if score == None:
            return NormalMessage.create_message(event, "スコアは登録されていません")

        return NormalMessage.create_message(event, f"あなたのスコアは{score}です。")
