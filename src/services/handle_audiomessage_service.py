import os
from vosk import Model, KaldiRecognizer
import pykakasi
import json
import asyncio
import aiofiles
import tempfile


class AudioMessageHandler:
    MAX_FILE_SIZE = 250 * 1024  # 250KB

    def __init__(self, line_bot_api, line_bot_blob_api, vosk_model_path):
        # Voskモデルのロード
        self.line_bot_api = line_bot_api
        self.line_bot_blob_api = line_bot_blob_api
        self.model = Model(vosk_model_path)
        self.kakasi = pykakasi.kakasi()

    async def process_audio_message(self, event):
        """
        音声データを受け取り、文字起こし結果を返す
        :param event: LINE APIからのevent
        :return: 認識結果（ひらがな）
        """
        message_content = self.line_bot_blob_api.get_message_content(
            message_id=event.message.id
        )

        # ファイルサイズチェック
        if len(message_content) > self.MAX_FILE_SIZE:
            return "もっと短くしゃべってほしいな"

        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".m4a"
        ) as temp_audio_file:
            temp_audio_path = temp_audio_file.name
            temp_audio_file.write(message_content)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
            wav_path = temp_wav_file.name

        try:
            # 音声ファイルを一時保存
            async with aiofiles.open(temp_audio_path, "wb") as temp_audio_file:
                temp_audio_file.write(message_content)

            # ffmpegでWAVに変換
            process = await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-y",
                "-i",
                temp_audio_path,
                "-ar",
                "16000",
                "-ac",
                "1",
                wav_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()

            # 音声認識の準備
            recognizer = KaldiRecognizer(self.model, 16000)

            # チャンクごとにデータを読み込み
            chunk_size = 8000  # 読み込むデータ量 (8000バイト = 約0.5秒分)
            buffer = b""  # バッファを初期化
            async with aiofiles.open(wav_path, "rb") as wav_file:
                while True:
                    data = await wav_file.read(chunk_size)
                    if not data:  # ファイルの終わりに到達
                        break

                    # バッファにデータを蓄積
                    buffer += data

                    # 十分なサイズがたまったら処理
                    if len(buffer) >= chunk_size:
                        recognizer.AcceptWaveform(buffer)
                        buffer = b""  # バッファをリセット

                # 最後に残ったデータを処理
                if buffer:
                    recognizer.AcceptWaveform(buffer)

            # 最終結果を取得
            result = json.loads(recognizer.FinalResult())
            transcript = result.get("text", "")

            return transcript if transcript else "クリアな音声でもう一回！"
        finally:
            # 一時ファイルのクリーンアップ
            for path in [temp_audio_path, wav_path]:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception as e:
                    print(f"一時ファイル削除エラー: {e}")

    def _convert_to_hiragana(self, text):
        """
        ローマ字や漢字をひらがなに変換
        :param text: 入力テキスト
        :return: ひらがな変換後のテキスト
        """
        result = self.kakasi.convert(text)
        return "".join([item["hira"] for item in result])
