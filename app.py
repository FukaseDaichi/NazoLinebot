import time
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    MessagingApiBlob,
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    TextMessageContent,
    AudioMessageContent,
    PostbackEvent,
)

import os
from flask import Flask, g, request, abort, render_template
import urllib3
from src.services.handle_postback_service import HandlePostbackService
from src.managers.gas_manager import GASManager
from src.managers.user_state_manager import UserStateManager
from src.services.handle_audiomessage_service import AudioMessageHandler
from src.services.handle_message_service import HandleMessageService
from src.commonclass.dict_not_notetion import DictDotNotation
from src.services.schedule import sched
from functools import wraps
from src.messages.messages_normal import Message as NormalMessage

## .env ファイル読み込み
from dotenv import load_dotenv

load_dotenv()

## 環境変数を変数に割り当て
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
GAS_API_URL = os.environ["GAS_API_URL"]

## Flask アプリのインスタンス化
app = Flask(__name__, static_folder="resources")

## LINE のアクセストークン読み込み
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

## APIインスタンス化
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    line_bot_blob_api = MessagingApiBlob(api_client)

## グローバル変数の初期化
gas_manager = GASManager(GAS_API_URL)
user_state_manager = UserStateManager(external_manager=gas_manager.get_user_name)

## handlerの初期化
handle_message_service = HandleMessageService()
handle_postback_service = HandlePostbackService()
audio_handler = AudioMessageHandler(
    line_bot_api, line_bot_blob_api, "./lib/model/vosk-model-small-ja-0.22"
)


## 共通全体処理
@app.before_request
def before_request():
    g.user_state_manager = user_state_manager
    g.gas_manager = gas_manager


def before_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        event = args[0]  # イベントオブジェクトの取得

        ## ユーザーIDの設定
        user_id = event.source.user_id if hasattr(event, "source") else "default_id"

        ## stateの取得
        state = user_state_manager.get_user_state(user_id)

        ## modeがないとき
        if state == None or "mode" not in state:

            ## モードをデフォルトで設定
            user_state_manager.set_user_state(user_id, {"mode": "default"})

            state = user_state_manager.get_user_state(user_id)

            ## nameの取得
            user_name = user_state_manager.get_user_name(user_id)

            ## ユーザ名がある場合メモリに格納
            if user_name:
                user_state_manager.set_user_state(user_id, {"user_name": user_name})
                g.user_name = user_name

        ## グローバルデータへ格納
        g.state = state
        g.user_id = user_id

        ## ユーザー名なしかつ、ユーザー名設定モードではない場合
        if g.state.get("user_name") == None and g.state.get("mode") != "set_user_name":
            user_state_manager.set_user_state(user_id, {"mode": "set_user_name"})
            reply_message(
                event,
                NormalMessage.create_message(
                    event, "初めまして!お名前を教えてください！"
                ),
            )
            return

        return func(*args, **kwargs)

    return wrapper


## 起動確認用ウェブサイトのトップページ
@app.route("/", methods=["GET"])
def topPage():
    return render_template("index.html")


## 動作確認用
## http://127.0.0.1:8000/test/help?mode=default&user_id=default_id
@app.route("/test/<text>", methods=["GET"])
def test(text):

    user_id = request.args.get("user_id")
    user_name = request.args.get("user_name")
    mode = request.args.get("mode")

    if user_id:
        g.user_id = user_id

        if mode:
            user_state_manager.set_user_state(user_id, {"mode": mode})
            g.state = user_state_manager.get_user_state(user_id)

        if user_name:
            user_state_manager.set_user_state(user_id, {"user_name": user_name})
        else:
            ## nameの取得
            user_name = user_state_manager.get_user_name(user_id)
            ## ユーザ名がある場合メモリに格納
            if user_name:
                user_state_manager.set_user_state(user_id, {"user_name": user_name})
                g.user_name = user_name

    event = DictDotNotation({"message": DictDotNotation({"text": text})})
    messages = handle_message_service.generate_reply_message(event)

    ##event = DictDotNotation({"postback": DictDotNotation({"data": text})})
    ##messages = handle_postback_service.generate_reply_message(event)

    if type(messages) == list:
        return {"messages": [message.to_dict() for message in messages]}

    return {"messages": [message.to_dict() for message in [messages]]}


## コールバック関数定義
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


## 友達追加時のメッセージ送信
@handler.add(FollowEvent)
def handle_follow(event):
    user_state_manager.set_user_state(event.source.user_id, {"mode": "set_user_name"})
    reply_message(
        event,
        NormalMessage.create_message(
            event,
            "こんにちは白いフラン謎へようこそ。まず名前を設定していただきます。あなたのお名前を教えてください",
        ),
    )


## テキストメッセージ
@handler.add(MessageEvent, message=TextMessageContent)
@before_handler
def handle_message(event, __destination=None):
    try:
        messages = handle_message_service.generate_reply_message(event)
        reply_message(event, messages)
    except Exception as e:
        error_handler(event, e)


# 音声メッセージハンドラー
@handler.add(MessageEvent, message=AudioMessageContent)
@before_handler
async def handle_voice(event, __destination=None):
    try:
        # process_audio_messageはasync関数
        response_text = await audio_handler.process_audio_message(event)
        reply_message(event, [TextMessage(text=response_text)])
    except Exception as e:
        error_handler(event, e)


## ポストバックハンドラー
@handler.add(PostbackEvent)
@before_handler
def handle_message(event, __destination=None):
    try:
        messages = handle_postback_service.generate_reply_message(event)
        reply_message(event, messages)
    except Exception as e:
        error_handler(event, e)


def reply_message(event, messages):
    try:
        if not isinstance(messages, list):
            messages = [messages]

        for _ in range(3):  # 最大3回リトライ
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(replyToken=event.reply_token, messages=messages)
                )
                break  # 成功したらループを抜ける
            except urllib3.exceptions.ProtocolError as e:
                app.logger.error(f"APIエラー {e}, retrying...")
                # 待機時間を設ける
                time.sleep(0.2)
                continue  # リトライ
    except Exception as e:
        error_handler(event, e)


def default_message(event):
    ## 受信メッセージの中身を取得
    received_message = event.message.text

    ## APIを呼んで送信者のプロフィール取得
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name

    ## 返信メッセージ編集
    reply = f"{display_name}さんのメッセージ\n{received_message}"
    reply_message(event, reply)


## ボット起動コード
if __name__ == "__main__":
    if not sched.running:  # スケジューラが実行中でない場合のみ開始
        sched.start()  # 追加
    ## ローカルでテストする時のために、`debug=True` にしておく
    app.run(host="0.0.0.0", port=8000, debug=True)


# エラーハンドラー
def error_handler(event, e):
    app.logger.error(f"Error sending reply message: {e}", exc_info=True)
    reply_message(event, NormalMessage.create_message(event, "例外が発生しました"))
