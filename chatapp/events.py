from flask_socketio import emit
from .extensions import socketio
from . import global_state
from .tts_config import create_text_to_speech
from .main_output_chatGPT import AI_chat_GPT
from .main_output_Mi7B import AI_chat_Mi7B

# socketの起動
@socketio.on("connect")
def handle_connect():
    print("Client connected")

#フロントからuser_inputを受け取り、GPTの起動
@socketio.on("user_input")
def ai_response(data):
    print("Reactからuser_inputを受け取りました。")
    if data:
        user_input = data
        selected_ai = global_state.ai_selection
        if selected_ai == "chat GPT":
            gpt_response, text_to_speech_data = AI_chat_GPT(user_input)
            socketio.emit("response_to_react",{"gpt_response":gpt_response, "text_to_speech_data":text_to_speech_data})
        elif selected_ai == "Mistral 7B":
            gpt_response, text_to_speech_data = AI_chat_Mi7B(user_input)
            socketio.emit("response_to_react",{"gpt_response":gpt_response, "text_to_speech_data":text_to_speech_data})
    else:
        print("Reactからuser_inputを受信できませんでした。")     

#フロントからai選択の入力を受け取り、global関数に反映
@socketio.on("ai_select")
def handle_ai_select(data):
    ai_select = data
    print("受け取ったai_select:",ai_select)
    global_state.ai_selection = ai_select

#フロントから言語選択の入力を受け取り、global関数に反映
@socketio.on("language_select")
def handle_language_select(data):
    language_select = data
    print("受け取ったlanguage_select:",language_select)
    global_state.language_selection = language_select

#フロントからモード選択の入力を受け取り、global関数に反映
@socketio.on("mode_select")
def handle_mode_select(data):
    mode_select = data
    print("受け取ったmode_select:",mode_select)
    global_state.mode_selection = mode_select

#フロントから翻訳時に出力する言語選択の入力を受け取り、global関数に反映
@socketio.on("out_language_select")
def handle_mode_select(data):
    out_language_select = data
    print("受け取ったmode_select:",out_language_select)
    global_state.out_language_selection = out_language_select

# welcome Messageの再生用
@socketio.on("welcome_message")
def handle_welcome_message(data):
    text_to_speech_data = create_text_to_speech(data)
    socketio.emit("play_welcome_message",{"text_to_speech_data":text_to_speech_data})
    







