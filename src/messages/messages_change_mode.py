from functools import partial
import threading
from flask import g
from src.messages.messages_normal import Message as NormalMessage


class Message:
    @staticmethod
    def create_message(event, obj=None):
        data = event.postback.data
        params = dict(x.split("=") for x in data.split("&"))
        mode = params.get("mode")

        ## 登録
        g.user_state_manager.set_user_state(g.user_id, {"mode": mode})

        ## スプレットシートへ記録
        # 値を束縛した新しい関数を作成
        target = partial(g.gas_manager.register_user, g.user_id, None, mode)
        # スレッドを作成して非同期で実行
        thread = threading.Thread(target=target)
        thread.start()

        return NormalMessage.create_message(
            event,
            "開始の準備が整いました。開始するには「スタート」と入力してください。そこからタイムが測定されます。",
        )
