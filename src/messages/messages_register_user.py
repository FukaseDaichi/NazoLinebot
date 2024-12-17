from urllib.parse import unquote
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, obj=None):
        data = event.postback.data
        params = dict(x.split("=") for x in data.split("&"))
        user_input = params.get("user_input")

        ## URLデコードを行う
        user_input = unquote(user_input)

        ## 登録
        g.user_state_manager.set_user_state(
            g.user_id, {"user_name": user_input, "mode": "default"}
        )
        
        target = g.gas_manager.register_user
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target, args=(g.user_id, user_input))
        thread.start()

        return NormalMessage.create_message(event, f"{user_input}で登録しました。")
