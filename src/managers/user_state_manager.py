import time


class UserStateManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(UserStateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, default_ttl=3600, external_manager=None):
        """
        ユーザー状態管理クラス
        :param default_ttl: 状態のデフォルト有効期限（秒）
        :param external_manager: 外部依存（テスト用）
        """
        # すでに初期化済みなら何もしない
        if self._initialized:
            return

        self.user_states = {}
        self.default_ttl = default_ttl
        self.external_manager = external_manager or self._default_external_manager

        # 初期化完了を示すフラグを更新
        self._initialized = True

    def _default_external_manager(self, user_id):
        """デフォルトの外部システム呼び出し（モック用）"""
        return None

    def cleanup_expired_states(self):
        """期限切れの状態を遅延削除"""
        current_time = time.time()
        expired_users = [
            user_id
            for user_id, state in self.user_states.items()
            if state["expiration_time"] <= current_time
        ]
        for user_id in expired_users:
            self.user_states.pop(user_id, None)

    def set_user_state(self, user_id, state, ttl=None):
        """ユーザー状態を設定（カスタムTTL対応）"""
        ttl = ttl or self.default_ttl
        expiration_time = time.time() + ttl
        pre_state = self.user_states.get(user_id, {}).get("state", {}) or {}
        pre_state.update(state)

        self.user_states[user_id] = {
            "state": pre_state,
            "expiration_time": expiration_time,
        }
        self.cleanup_expired_states()  # 遅延クリーンアップ

    def get_user_state(self, user_id):
        """ユーザー状態を取得"""
        state_data = self.user_states.get(user_id)
        if not state_data or state_data["expiration_time"] <= time.time():
            self.user_states.pop(user_id, None)
            return None
        self.cleanup_expired_states()  # 遅延クリーンアップ
        return state_data["state"]

    def extend_user_ttl(self, user_id, ttl=None):
        """ユーザー状態のTTLを延長"""
        if user_id in self.user_states:
            ttl = ttl or self.default_ttl
            self.user_states[user_id]["expiration_time"] = time.time() + ttl
            self.cleanup_expired_states()

    def get_user_name(self, user_id):
        """ユーザー名を取得"""
        state = self.get_user_state(user_id)
        if state and "user_name" in state:
            return state["user_name"]

        # 外部依存から取得
        user = self.external_manager(user_id)
        user_name = user.get("name") if user and "name" in user else None

        if user_name:
            self.set_user_state(user_id, {"user_name": user_name})
        return user_name

    def get_user(self, user_id):
        """ユーザー名を取得"""
        state = self.get_user_state(user_id)
        if state and "user_name" in state:
            return state

        # 外部依存から取得
        print("スプレットシートから取得")
        user = self.external_manager(user_id)
        print(user)
        user_name = user.get("name") if user and "name" in user else None
        mode = user.get("mode") if user and "mode" in user else None

        state = {}
        if user_name:
            state["user_name"] = user_name

        if mode:
            state["mode"] = mode
        else:
            state["mode"] = "default"

        self.set_user_state(user_id, state)

        return state
