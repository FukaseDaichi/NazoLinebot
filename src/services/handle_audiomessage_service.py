import uuid
import os
import subprocess
from vosk import Model
from vosk import Model, KaldiRecognizer
import pykakasi
import json
import tempfile

## https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-kitchensink/app.py
class AudioMessageHandler:
    def __init__(self, line_bot_api, line_bot_blob_api, vosk_model_path):
        # Voskモデルのロード
        self.line_bot_api = line_bot_api
        self.line_bot_blob_api = line_bot_blob_api
        self.model = Model(vosk_model_path)
        self.kakasi = pykakasi.kakasi()

    def process_audio_message(self, event):
        """
        音声データを受け取り、文字起こし結果を返す
        :param event: LINE APIからのevent
        :return: 認識結果（ひらがな）
        """
        message_content = self.line_bot_blob_api.get_message_content(
            message_id=event.message.id
        )

        # ユニークなファイル名を生成
        temp_audio_path = f"/tmp/{uuid.uuid4()}.m4a"
        wav_path = f"/tmp/{uuid.uuid4()}.wav"

        try:
            # tempfileを使って一時ファイルを生成
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_audio_file:
                temp_audio_file.write(message_content)
                temp_audio_path = temp_audio_file.name

            # WAVファイルパスもtempfileで生成
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
                wav_path = temp_wav_file.name

            # m4aをWAVに変換
            subprocess.run(
                ["ffmpeg", "-i", temp_audio_path, "-ar", "16000", "-ac", "1", wav_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # 音声認識
            recognizer = KaldiRecognizer(self.model, 16000)
            with open(wav_path, "rb") as wav_file:
                while True:
                    data = wav_file.read(4000)
                    if len(data) == 0:
                        break
                    recognizer.AcceptWaveform(data)

            # 認識結果を取得
            result = json.loads(recognizer.FinalResult())
            transcript = result.get("text", "")

            # ひらがな変換
            if transcript:
                return self._convert_to_hiragana(transcript)
            else:
                return "音声を認識できませんでした。"
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            print(f"ffmpeg stderr: {e.stderr.decode()}") # ffmpegのエラー出力を表示
            return f"エラーが発生しました: {str(e)}"
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def _convert_to_hiragana(self, text):
        """
        ローマ字や漢字をひらがなに変換
        :param text: 入力テキスト
        :return: ひらがな変換後のテキスト
        """
        result = self.kakasi.convert(text)
        return "".join([item["hira"] for item in result])
