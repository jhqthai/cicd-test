# dew-backend

Dew-backend utilising IBM Watson STT(Speech-to-Text) API to transform interview audio data:
https://cloud.ibm.com/apidocs/speech-to-text

### How to install
Locally: 
- Install Python
- cd to /backend folder
- Run pip install -r requirements.txt
### How to run
Locally: 
- Run "set FLASK_ENV=development" command
- Run with "python -m flask run" command
- [Backend URL](http://localhost:5000)
- Use in conjunction with [DEW-UI Frontend](https://dew-ui.lmo02ivce3a.au-syd.codeengine.appdomain.cloud/) to upload an interview mp3 audio file and download the transcription in CSV format
