from flask import g
import redis
import os
import json

class UserStateManager:
    def __init__(self, redis_url=None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.StrictRedis.from_url(
            self.redis_url, decode_responses=True
        )
        self.default_ttl = 3600  # 状態の有効期限（秒）

    def set_user_state(self, user_id, state):
        """
        ユーザーの状態を設定
        """
        key = f"user_state:{user_id}"

              # 既存の状態を取得
        current_state = self.get_user_state(user_id)
        
        # 既存の状態が存在する場合は、新しい状態とマージ
        if current_state:
            current_state.update(state)
            state = current_state
        
        self.redis_client.set(key, json.dumps(state), ex=self.default_ttl)

    def get_user_state(self, user_id):
        """
        ユーザーの状態を取得
        """
        key = f"user_state:{user_id}"
        state = self.redis_client.get(key)
        return json.loads(state) if state else None

    def delete_user_state(self, user_id):
        """
        ユーザーの状態を削除
        """
        key = f"user_state:{user_id}"
        self.redis_client.delete(key)

    def extend_user_ttl(self, user_id):
        """
        ユーザーの状態のTTLを延長
        """
        key = f"user_state:{user_id}"
        self.redis_client.expire(key, self.default_ttl)
    
    def get_user_name(self, user_id):
        state = self.get_user_state(user_id)
        ## stateがある場合ユーザー名を取得
        if state:
            user_name = state.get("user_name")
        
        ## ユーザー名がある場合そのまま返す
        if user_name:
            return user_name

        ## ユーザー名がない場合スプレットシートから取得   
        user_name = g.gas_manager.get_user_name(user_id)

        ## 取得できた場合、設定する
        if user_name:
            self.set_user_state(user_id,{"user_name": user_name})
            return user_name
        
        ## 何もない場合Noneを返す
        return None
