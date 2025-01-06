from flask import g
from src.messages.messages_normal import Message as NormalMessage


class Message:
    @staticmethod
    def create_message(event, args=None):
        """
        args[0]はtitleとする。
        """
        # 値を束縛した新しい関数を作成
        result = g.gas_manager.get_user_score(g.user_id, args[0])
        if result == None:
            return NormalMessage.create_message(event, "スコアは登録されていません")
        score = result["score"]
        return NormalMessage.create_message(event, f"あなたのスコアは{score}です。")
