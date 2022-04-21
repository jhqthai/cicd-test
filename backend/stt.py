from ibm_watson import SpeechToTextV1
import pandas as pd
import os
import io
from bisect import bisect_right
import json
from typing import BinaryIO
import requests
import flask
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time


API_KEY = "ke-xv2LWvs5SO4ZuUcaGTe3ycMEQfP9-wrh6me63Koxw"
CLOUD_ENDPOINT = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/a07b06d2-85d9-48c9-b451-a01df06bdc1b"
UPLOAD_FOLDER = "/transcribe/upload-audio/"
MP3_FILE_NAME = ""


def watson_batch_stt(filename, lang: str, encoding: str) -> str:
    authenticator = IAMAuthenticator(API_KEY)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(CLOUD_ENDPOINT)
    audio_file = filename.read()
    response = speech_to_text.recognize(
        audio=audio_file,
        # content_type='audio/{}'.format(os.path.splitext(filename)[1][1:]),
        content_type='audio/mp3',
        model=lang + '_Multimedia',
        max_alternatives=0,
        speaker_labels=True,
        inactivity_timeout=-1,
        low_latency=False
    ).get_result()

    return response

# *** STT an mp3 uploaded from frontend and parse it to csv file


def main(audio_file_name):
    SpeechToTextResults = watson_batch_stt(
        audio_file_name, 'en-AU', 'UTF-8')
    jsonconvo = json.dumps(SpeechToTextResults)

    jsonconvo = json.loads(jsonconvo)
    speakers = pd.DataFrame(jsonconvo['speaker_labels']).loc[:, [
        'from', 'speaker', 'to']]
    data = []
    for alts in jsonconvo['results']:
        for i in alts['alternatives']:
            data.extend(i['timestamps'])
    convo = pd.DataFrame(data)
    speakers = speakers.join(convo)

    ChangeSpeaker = speakers.loc[speakers['speaker'].shift(
    ) != speakers['speaker']].index

    Transcript = pd.DataFrame(columns=['from', 'to', 'speaker', 'transcript'])
    for counter in range(0, len(ChangeSpeaker)):
        currentindex = ChangeSpeaker[counter]
        try:
            nextIndex = ChangeSpeaker[counter+1]-1
            temp = speakers.loc[currentindex:nextIndex, :]
        except:
            temp = speakers.loc[currentindex:, :]

        Transcript = pd.concat([Transcript, pd.DataFrame([[temp.head(1)['from'].values[0], temp.tail(1)['to'].values[0], temp.head(1)[
            'speaker'].values[0], ' '.join(temp[0].tolist())]], columns=['from', 'to', 'speaker', 'transcript'])])

        only_transcript = Transcript.loc[:, ["speaker", "transcript"]]
    stream = io.StringIO()
    Transcript.to_csv(stream, sep=",")
    return stream
