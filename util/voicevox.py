from functools import cache

import requests

from util import env


class VoiceVox():
    def __init__(self) -> None:
        self.URL = env.VOICEVOX_BASE_URL
        self.speaker = 1
        self.CORE_VERSION = self._get_core_version()

    def test(self):
        print(self.CORE_VERSION)


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

    def _get_core_version(self):
        req_url = f"{self.URL}core_versions"
        response = requests.get(req_url)
        return response.json()[0]


    def __get_speaker_list(self) -> list:
        url = f"{self.URL}speakers"
        params = {
            'core_version': self.CORE_VERSION
        }
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    
    @cache
    def __speaker_dict(self) -> dict:
        """
        return speaker_dict
        ex)
        {"四国めたん" : {"あまあま":2, "あまあま":0}, "ずんだもん" : {"あまあま":2, "あまあま":0}}
        """
        speaker_dict = {}
        speaker_list = self.__get_speaker_list()
        # print(speaker_list[0]["styles"])
        for i in range(len(speaker_list)):
            # print(speaker_list[i]["name"])
            styles_list = speaker_list[i]["styles"]
            style_dict = {}
            # speaker_dict[speaker_list[i]["name"]] = styles_list
            for j in range(len(styles_list)):
                style_dict[styles_list[j]["name"]] = styles_list[j]["id"]
            speaker_dict[speaker_list[i]["name"]] = style_dict

        return speaker_dict
    
    def speaker_list(self) -> list:
        return list(self.__speaker_dict().keys())
    
    def speaker2styles(self, speaker_name) -> dict:
        return self.__speaker_dict()[speaker_name]

    def style2id(self, speaker_name,  style) -> int:
        return self.speaker2styles(speaker_name)[style]
