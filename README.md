# asr-service

`POST /`
#### <b>Parameter</b>
* **language** : _language used in audio, default None (use language detection)_ <br>
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