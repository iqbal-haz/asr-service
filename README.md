# asr-service

## Installation

1. Clone repository
2. Create virutal environment <br>
Python setup <br>
`python3 -m venv env` <br>
Virtualenv <br>
`virtualenv env`
3. Activate virtual environment <br>
Windows <br>
`env\Scripts\activate` <br>
MacOS / Linux <br>
`source env/bin/activate`
4. Install requirements <br>
`pip install -r requirements.txt`
5. Run the app <br>
`flask run`

## Endpoint(s)

`POST /`
#### <b>Parameter</b>
* **language** (optional): _language spoken in audio, default None (automatically use language detection)_ <br>
Please refer [here](https://github.com/openai/whisper#available-models-and-languages) for available language choices.

No parameter
```
curl --location --request POST 'http://127.0.0.1:5000/' \
--form 'audio=@"/path/to/audio/file"'
```

With parameter
```
curl --location --request POST 'http://127.0.0.1:5000/?language=en' \
--form 'audio=@"/path/to/audio/file"'
```
