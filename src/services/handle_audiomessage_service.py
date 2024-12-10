# import whisper

# class HandleAudioMessageService:

#     @staticmethod
#     def generate_reply_message(event):
#         audio_file_path = "path/to/audio_file.mp3"  # 音声ファイルのパスを指定    # Whisperモデルをロード
#         model = whisper.load_model("base")
#         # 音声ファイルを文字起こし
#         result = model.transcribe(audio_file_path, language="ja")
#         # 文字起こし結果を返す
#         return result["text"]
