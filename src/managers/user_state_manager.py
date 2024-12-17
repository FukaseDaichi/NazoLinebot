import threading
import time


class UserStateManager:
    def __init__(self, cleanup_interval=3600, default_ttl=3600, external_manager=None):
        """
        初期化時にスレッドを起動し、状態をクリーンアップする。
        :param cleanup_interval: クリーンアップ間隔（秒）
        :param default_ttl: 状態のデフォルト有効期限（秒）
        :param external_manager: 外部依存（テスト用）
        """
        self.user_states = {}
        self.lock = threading.Lock()
        self.default_ttl = default_ttl
        self.cleanup_interval = cleanup_interval
        self.stop_event = threading.Event()
        self.external_manager = external_manager or self._default_external_manager

        # クリーンアップスレッドを起動
        self.cleanup_thread = threading.Thread(target=self._cleanup_task, daemon=True)
        self.cleanup_thread.start()

    def _default_external_manager(self, user_id):
        """デフォルトの外部システム呼び出し（モック用）"""
        return None

    def _cleanup_task(self):
        """定期的に期限切れの状態をクリーンアップするタスク"""
        while not self.stop_event.is_set():
            try:
                self.cleanup_expired_states()
                time.sleep(self.cleanup_interval)
            except Exception as e:
                # ログや再試行ロジックを追加可能
                print(f"Cleanup thread error: {e}")

    def stop_cleanup_thread(self):
        """クリーンアップスレッドを停止"""
        self.stop_event.set()
        self.cleanup_thread.join()

    def cleanup_expired_states(self):
        """期限切れの状態を削除"""
        with self.lock:
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
        with self.lock:
            ttl = ttl or self.default_ttl
            expiration_time = time.time() + ttl
            self.user_states[user_id] = {
                "state": state,
                "expiration_time": expiration_time,
            }

    def get_user_state(self, user_id):
        """ユーザー状態を取得"""
        with self.lock:
            state_data = self.user_states.get(user_id)
            if not state_data or state_data["expiration_time"] <= time.time():
                self.user_states.pop(user_id, None)
                return None
            return state_data["state"]

    def extend_user_ttl(self, user_id, ttl=None):
        """ユーザー状態のTTLを延長"""
        with self.lock:
            if user_id in self.user_states:
                ttl = ttl or self.default_ttl
                self.user_states[user_id]["expiration_time"] = time.time() + ttl

    def get_user_name(self, user_id):
        """ユーザー名を取得"""
        state = self.get_user_state(user_id)
        if state and "user_name" in state:
            return state["user_name"]

        # 外部依存から取得
        user_name = self.external_manager(user_id)
        if user_name:
            self.set_user_state(user_id, {"user_name": user_name})
        return user_name
