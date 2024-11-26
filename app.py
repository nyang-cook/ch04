import streamlit as st
from st_audiorecorder import audio_recorder

st.title("Audio Recorder Test")

# Record audio
audio = audio_recorder()

if audio:
    # Save the recorded audio
    with open("recorded_audio.wav", "wb") as f:
        f.write(audio)
    st.audio("recorded_audio.wav", format="audio/wav")
    st.success("Audio recorded and saved successfully!")
