import os
import firebase_admin
from firebase_admin import credentials, firestore
import time


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

    def format_seconds_to_japanese_time(self, seconds):
        """秒数（int）を「??分??秒」の文字列に変換する"""
        if seconds is None:
            return "記録なし"
        minutes = seconds // 60
        sec = seconds % 60
        if minutes > 0:
            return f"{minutes}分{sec}秒"
        else:
            return f"{sec}秒"

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
        """ゲームを開始する（データが存在しない場合のみ）"""
        doc_ref = self.db.collection(title).document(user_id)
        doc = doc_ref.get()

        if not doc.exists:
            new_game = {
                "title": title,
                "start": int(time.time()),
                "end": None,
                "score": None,
            }

            doc_ref.set(new_game, merge=False)  # データがないときだけセット

    def end_game(self, title, user_id):
        """ゲームの終了を記録し、スコアを計算する"""
        doc_ref = self.db.collection(title).document(user_id)
        doc = doc_ref.get()

        # データが存在しない場合は何もしない
        if not doc.exists:
            return

        data = doc.to_dict()
        start_time = data.get("start")
        if start_time is None:
            return  # startがなければスコア計算不可

        # scoreが既にあれば終了
        if data.get("score"):
            return

        end_time = int(time.time())
        score = end_time - start_time  # 秒数で計算

        # Firestoreにendとscoreを保存
        doc_ref.update({"end": end_time, "score": score})

    def get_user_score(self, user_id, title):
        """ユーザーの特定のゲームのスコアを取得する"""
        doc_ref = self.db.collection(title).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return self.format_seconds_to_japanese_time(data.get("score"))
        return None

    def get_score(self, title):
        """特定のゲームの全ユーザーのスコアランキングを取得する"""
        title_ref = self.db.collection(title)
        title_docs = title_ref.stream()

        users_ref = self.db.collection("users")
        scores = []

        for doc in title_docs:
            game_data = doc.to_dict()
            user_id = doc.id

            # スコアが存在しない場合はスキップ
            if game_data.get("score") is None:
                continue

            # ユーザー名をゲームデータから取得、なければusersコレクションから取得
            name = ""
            user_doc = users_ref.document(user_id).get()
            if user_doc.exists:
                name = user_doc.to_dict().get("name")
            else:
                name = "Unknown"

            scores.append(
                {
                    "name": name,
                    "score": self.format_seconds_to_japanese_time(game_data["score"]),
                }
            )

        # スコアで昇順にソートし、最大5件を返す
        return sorted(scores, key=lambda x: x["score"])[:5]


if __name__ == "__main__":
    # Example usage:
    # 環境変数の設定が必要
    # os.environ["FIREBASE_CREDENTIALS_PATH"] = "path/to/your/firebase-credentials.json"
    # fb_manager = FirebaseManager()
    # fb_manager.register_user("test_user_id", name="Test User", mode="easy")
    # user_info = fb_manager.get_user("test_user_id")
    # print(user_info)
    pass
