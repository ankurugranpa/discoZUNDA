# discoZunda
[Japanese README.md](./README_ja.md)
## Requierment
- You need poetry
```
pip install poetry
```
- voice client support 
You need to install `libffi-dev` and `ffmpeg`.

- You need VoiceVox EngineAPI
[VOICEVOX/voicevox_engine](https://github.com/VOICEVOX/voicevox_engine)
use with docker 
```
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```

## How to Use
```
git clone git@github.com:ankurugranpa/discoZUNDA.git
cd discoZUNDA
python3 -m poetry install 
cp .env.exsample .env
## you need setting .env file ##
python3 -m poetry run python3 main.py
```
