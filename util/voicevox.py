import requests

from util import env


class VoiceVox():
    def __init__(self) -> None:
        self.URL = env.VOICEVOX_BASE_URL

    def req_voice(self, voice_text:str):
        params = {
            'text': voice_text
        }

        # POSTリクエストを送信
        response = requests.post(f'{self.URL}audio_query?speaker=1', params=params)
        query = response.json()

        headers = {'Content-Type': 'application/json'}
        # POSTリクエストを送信
        voice = requests.post(f"{self.URL}synthesis?speaker=1", headers=headers, json=query)
        return voice.content

if __name__=="__main__":
    voice_vox = VoiceVox()
    source = voice_vox.req_voice("おなかすいたご飯何?")
    with open('./output.wav', 'wb') as f:
        f.write(source)
    print("WAVファイルが正常に保存されました。")
