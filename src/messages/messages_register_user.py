from functools import partial
from urllib.parse import unquote
from flask import g
from src.messages.messages_normal import Message as NormalMessage
import threading


class Message:
    @staticmethod
    def create_message(event, obj=None):
        ## ユーザー名設定ではない場合
        if g.state.get("mode") != "set_user_name":
            user_name = g.user_state_manager.get_user_name(g.user_id)
            return NormalMessage.create_message(
                event, f"{user_name}さんですでに登録してます。"
            )

        data = event.postback.data
        params = dict(x.split("=") for x in data.split("&"))
        user_input = params.get("user_input")

        ## URLデコードを行う
        user_input = unquote(user_input)
        ## 登録
        g.user_state_manager.set_user_state(
            g.user_id, {"user_name": user_input, "mode": "default"}
        )
        # 値を束縛した新しい関数を作成
        target = partial(g.gas_manager.register_user, g.user_id, user_input)
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target)
        thread.start()

        return NormalMessage.create_message(event, f"{user_input}で登録しました。")
