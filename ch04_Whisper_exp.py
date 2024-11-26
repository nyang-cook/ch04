from openai import OpenAI

client = OpenAI(api_key="키를 입력해주세요")

audio_file = open("speech.mp3", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)

print(transcript)