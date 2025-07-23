import os
import firebase_admin
from firebase_admin import credentials, firestore


class FirebaseManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        import base64
        import json

        cred_base64 = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
        if not cred_base64:
            raise ValueError(
                "FIREBASE_CREDENTIALS_BASE64 environment variable not set."
            )

        try:
            cred_json_str = base64.b64decode(cred_base64).decode("utf-8")
            cred_info = json.loads(cred_json_str)
        except Exception as e:
            raise ValueError(
                f"Failed to decode or parse FIREBASE_CREDENTIALS_BASE64: {e}"
            )

        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self._initialized = True
        print("FirebaseManager initialized.")

    def get_user(self, user_id):
        """ユーザー情報を取得する"""
        doc_ref = self.db.collection("users").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    def get_user_name(self, user_id):
        """ユーザー名を取得する"""
        user_data = self.get_user(user_id)
        return user_data.get("name") if user_data else None

    def register_user(self, user_id, name=None, mode=None):
        """ユーザーを登録または更新する"""
        doc_ref = self.db.collection("users").document(user_id)
        data = {}
        if name is not None:
            data["name"] = name
        if mode is not None:
            data["mode"] = mode

        if data:
            doc_ref.set(data, merge=True)

    def start_game(self, title, user_id):
        """ゲームの開始を記録する"""
        doc_ref = self.db.collection("users").document(user_id)
        new_game = {
            "title": title,
            "start": firestore.SERVER_TIMESTAMP,
            "end": None,
            "score": None,
        }
        doc_ref.update({"games": firestore.ArrayUnion([new_game])})

    def end_game(self, title, user_id):
        """ゲームの終了を記録し、スコアを計算する"""
        doc_ref = self.db.collection("users").document(user_id)
        user_data = self.get_user(user_id)
        if not user_data or "games" not in user_data:
            return

        games = user_data["games"]
        game_to_update = None
        for game in reversed(games):  # 最後に追加されたものから探す
            if game["title"] == title and game["end"] is None:
                game_to_update = game
                break

        if game_to_update:
            start_time = game_to_update["start"]
            end_time = firestore.SERVER_TIMESTAMP

            # Firestoreのサーバータイムスタンプを一度書き込んでからでないと正確な計算ができない
            # ここではまず終了時刻を記録する
            game_to_update["end"] = end_time

            # スコア計算ロジック（例：秒単位）
            # 正確なスコア計算は、end_timeが確定した後（読み取り後）に行う必要がある
            # ここでは仮にNoneとしておくか、別途バッチ処理などで計算する方が堅牢
            # score = (end_time - start_time).total_seconds()
            # game_to_update["score"] = score

            doc_ref.update({"games": games})

    def get_user_score(self, user_id, title):
        """ユーザーの特定のゲームの最新スコアを取得する"""
        user_data = self.get_user(user_id)
        if not user_data or "games" not in user_data:
            return None

        user_games = [
            g
            for g in user_data["games"]
            if g["title"] == title and g["score"] is not None
        ]
        if not user_games:
            return None

        # 最新のゲーム（startが最も新しい）のスコアを返す
        latest_game = max(user_games, key=lambda x: x["start"])
        return latest_game["score"]

    def get_score(self, title):
        """特定のゲームの全ユーザーのスコアランキングを取得する"""
        users_ref = self.db.collection("users")
        docs = users_ref.stream()

        scores = []
        for doc in docs:
            user_data = doc.to_dict()
            if "games" in user_data and "name" in user_data:
                user_games = [
                    g
                    for g in user_data["games"]
                    if g["title"] == title and g["score"] is not None
                ]
                if user_games:
                    # ユーザーごとに最新のスコアを採用
                    latest_game = max(user_games, key=lambda x: x["start"])
                    scores.append(
                        {"name": user_data["name"], "score": latest_game["score"]}
                    )

        # スコアで降順にソート
        return sorted(scores, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    # Example usage:
    # 環境変数の設定が必要
    # os.environ["FIREBASE_CREDENTIALS_PATH"] = "path/to/your/firebase-credentials.json"
    # fb_manager = FirebaseManager()
    # fb_manager.register_user("test_user_id", name="Test User", mode="easy")
    # user_info = fb_manager.get_user("test_user_id")
    # print(user_info)
    pass
