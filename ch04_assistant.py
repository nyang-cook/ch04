#### 기본정보 입력 ####
# 스트림릿 패키지 
import streamlit as st
from audio_recorder_streamlit import audio_recorder

# OpenAI 패키지 추가
from openai import OpenAI

# 파이썬 기본 패키지
import os
import base64
import numpy as np

#### 기능 구현 함수 ####
# 음성을 텍스트로 변환하는 STT API
def STT(audio, client):
    # Whisper API가 파일 형태로 음성을 입력받으므로 input.mp3 파일을 저장
    filename='input.mp3'
    wav_file = open(filename, "wb")
    wav_file.write(audio.export().read())
    wav_file.close()

    # 음성 파일 열기
    audio_file = open(filename, "rb")
    # whisper 모델을 활용하여 텍스트 얻기
    try:
        # openai와 whisper api를 활용하여 텍스트를 추출합니다.
        transcript = client.audio.transcriptions.create(
            model = "whisper-1",
            file = audio_file,
            response_format='text'
        )
        audio_file.close()
        os.remove(filename)
    except:
        transcript = "API Key를 확인해주세요"
    return transcript

# 텍스트를 음성으로 변환하는 TTS API
def TTS(response, client):
    # TTS를 활용하여 만든 음성을 파일로 저장
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input=response,
    ) as response:
        filename = "output.mp3"
        response.stream_to_file(filename)

    # 저장한 음성 파일을 자동 재생
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

        # 스트림릿에서 음성 자동 재생
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True,)
    # 폴더에 남지 않도록 파일을 삭제
    os.remove(filename) 

# 음성 비서의 답변을 생서하는 Chatgpt api
def ask_gpt(prompt, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return response.choices[0].message.content       
    



