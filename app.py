from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    PostbackAction,
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    TextMessageContent,
    AudioMessageContent,
)
import os
from flask import Flask, request, abort, render_template
from src.services.handle_audiomessage_service import AudioMessageHandler
from src.services.handle_message_service import HandleMessageService
from src.commonclass.dict_not_notetion import DictDotNotation
from src.services.schedule import sched

## .env ファイル読み込み
from dotenv import load_dotenv

load_dotenv()

## 環境変数を変数に割り当て
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

print(CHANNEL_ACCESS_TOKEN)
print(CHANNEL_SECRET)

# AudioMessageHandlerの初期化
audio_handler = AudioMessageHandler("./lib/model/vosk-model-small-ja-0.22")

## Flask アプリのインスタンス化
app = Flask(__name__)

## LINE のアクセストークン読み込み
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


## 起動確認用ウェブサイトのトップページ
@app.route("/", methods=["GET"])
def topPage():
    return render_template("index.html")


# 動作確認用
@app.route("/test//<text>", methods=["GET"])
def test(text):
    event = DictDotNotation({"message": DictDotNotation({"text": text})})
    messages = HandleMessageService.generate_reply_message(event)
    print("こんいちは")

    if type(messages) == list:
        return {"messages": [message.as_json_dict() for message in messages]}

    return {"messages": [message.as_json_dict() for message in [messages]]}


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
    ## APIインスタンス化
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    ## 返信
    line_bot_api.reply_message(
        ReplyMessageRequest(
            replyToken=event.reply_token, messages=[TextMessage(text="Thank You!")]
        )
    )

## テキストメッセージ
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    ## APIインスタンス化
    messages = HandleMessageService.generate_reply_message(event)
    reply_message(event, [TextMessage(text=messages)])

# 音声メッセージハンドラー
@handler.add(MessageEvent, message=AudioMessageContent)
def handle_voice(event):
    # 音声データを取得
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    message_content = line_bot_api.get_message_content(event.message.id)
    # handle_audiomessage_service.pyで音声処理
    response_text = audio_handler.process_audio_message(message_content)
    reply_message(event, [TextMessage(text=response_text)])

def reply_message(event, messages):
    ## APIインスタンス化
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    line_bot_api.reply_message(
        ReplyMessageRequest(replyToken=event.reply_token, messages=messages)
    )


def defolt_message(event):
    ## APIインスタンス化
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

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
def error_handler(event,message):
    if message:
        print(message)
    reply_message(event,"例外が発生しました。")
    