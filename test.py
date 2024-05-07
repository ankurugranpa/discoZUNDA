from util.voicevox import VoiceVox

voice_vox = VoiceVox()
# source = voice_vox.req_voice("おなかすいたご飯何?")
# with open('./output.wav', 'wb') as f:
#     f.write(source)
# print("WAVファイルが正常に保存されました。")
# voice_vox.test()
# print(voice_vox._get_speaker_json())
voice_vox.create_speaker_json()
