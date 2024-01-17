import os
import requests
from dotenv import load_dotenv
from .tts_config import create_text_to_speech
from . import global_state


def AI_chat_Mi7B(voice_input):
    load_dotenv()
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    # マイクから取ってきたものを関数化
    user_input = voice_input
    if user_input:
        print(f"AI_selected{global_state.ai_selection}")
        print(f"Language_selected{global_state.language_selection}")
        print(f"Mode_selected{global_state.mode_selection}")
        print(f"You:{user_input}")
    else: 
        print("user_inputを受け取っていません")    
    
    # ----------------------- perplexityAI api の設定 ---------------------------
    url = "https://api.perplexity.ai/chat/completions"
    ai_prompt = "You are a friendly language teacher. Your response must be less than 50 words."
    if global_state.mode_selection == "Translate":
        ai_prompt = f"Translate the given input to {global_state.out_language_selection}. Do not include anything else."    
    payload = {
        "model": "llama-2-70b-chat",
        "messages": [
            {
                "role": "system",
                "content": ai_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "max_tokens":150
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {PERPLEXITY_API_KEY}"
    }
   
    gpt_response = None
    text_to_speech_data = None
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # aiから生成されたものから文字部分のみ抽出
        response_json = response.json()
        gpt_response = response_json["choices"][0]["message"]["content"]
        print(f"AI:{gpt_response}") 
        text_to_speech_data = create_text_to_speech(gpt_response)
    else:
        print(f"Error: Received status code {response.status_code}")  
                             
    return gpt_response, text_to_speech_data
 
