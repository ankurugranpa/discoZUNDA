import json

import requests

from util import env


class VoiceVox():
    def __init__(self) -> None:
        self.URL = env.VOICEVOX_BASE_URL
        self.speaker = 1
        self.core_versions = self._get_core_version()

    def test(self):
        print(self.core_versions)


    def req_voice(self, voice_text:str):
        params = {
            'text': voice_text
        }

        # POSTリクエストを送信
        response = requests.post(f'{self.URL}audio_query?speaker={self.speaker}', params=params)
        query = response.json()

        headers = {'Content-Type': 'application/json'}
        # POSTリクエストを送信
        voice = requests.post(f"{self.URL}synthesis?speaker={self.speaker}", headers=headers, json=query)
        return voice.content

    def set_speaker(self, speaker_num:int):
        self.speaker = speaker_num

    def speaker_dict(self, speaker_num):
        return

    def _get_core_version(self):
        req_url = f"{self.URL}core_versions"
        response = requests.get(req_url)
        return response.json()[0]


    def _get_speaker_list(self):
        url = f"{self.URL}speakers"
        params = {
            'core_version': self.core_versions
        }
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    
    def create_speaker_json(self):
        speaker_list = self._get_speaker_list()
        print(speaker_list[2]["styles"])
