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
        messages = [
            "開始の準備が整いました。開始するには「スタート」と入力してください。そこからタイムが測定されます。",
            "1時間ほど何も入力しないで放置すると、ゲーム選択からやり直しになります。これは謎には関係のない仕様です。",
        ]
        return NormalMessage.create_message(event, messages)
