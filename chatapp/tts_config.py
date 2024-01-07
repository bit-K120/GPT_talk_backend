import pygame.mixer
from google.cloud import texttospeech
import os
import json
import tempfile
from dotenv import load_dotenv
from . import global_state
import base64


load_dotenv()
google_cloud_keyfile_json = os.getenv("GOOGLE_CLOUD_KEYFILE_JSON")
if not google_cloud_keyfile_json:
    google_cloud_keyfile_json = os.getenv("GOOGLE_API_KEY")

if google_cloud_keyfile_json:
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(google_cloud_keyfile_json)
        temp_file_path = temp_file.name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path


def create_text_to_speech(gpt_response):
    language_selected = global_state.language_selection
    voice_language = ""
    if language_selected == "English":
        voice_language = "en-GB"
    elif language_selected == "French":
        voice_language = "fr-FR"
    elif language_selected == "Japanese":
        voice_language = "ja-JP"
    
    # google text to speechのクライアントを起動
    client = texttospeech.TextToSpeechClient()
    # 発生する声の設定
    synthesis_input = texttospeech.SynthesisInput(text=gpt_response)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_language,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    # 出力する音声ファイルの設定
    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )
    # APIに接続
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config= audio_config)
    text_to_speech_data = base64.b64encode(response.audio_content).decode("utf-8")
    return text_to_speech_data
    # 音声ファイルを保存
    # if os.path.exists("output.mp3"):
    #     os.remove("output.mp3")
    # with open("output.mp3", "wb") as out:
    #     out.write(response.audio_content)
    


# 音声を生成するのと再生するのは別々だからplay_voiceで音声の再生も作る。
def play_voice():
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # ファイルを消す前にアンロードさせる
    pygame.mixer.music.unload()
    # スピーチが起きる度に毎回output.mp3を消す
   

