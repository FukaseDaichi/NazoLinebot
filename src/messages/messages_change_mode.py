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
        return NormalMessage.create_message(
            event,
            "開始の準備が整いました。開始するには「スタート」と入力してください。そこからタイムが測定されます。",
        )
