import os
from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import logging

# Load variable enviroment
load_dotenv()

# Config loggin
logging.basicConfig(
    level=logging.INFO,
    format='mensaje: [%(message)s] ***** fecha_ejecucion: [%(asctime)s]',
    datefmt='%d/%m/%y - %H:%M:%S',
    filename='./logs/logs.txt'
)
logger = logging.getLogger(__name__)

api_transcription = os.getenv('api_transcription')
pass_api_transcription = os.getenv('pass_api_transcription')
api_translate = os.getenv('api_translate')
pass_api_translate = os.getenv('pass_api_translate')
version_api_translate = os.getenv('version_api_translate')


def transcript_audio(file_to_transcript: str):
    authenticator = IAMAuthenticator(apikey=pass_api_transcription)
    speech_transcription = SpeechToTextV1(authenticator=authenticator)
    speech_transcription.set_service_url(api_transcription)
    text_transcribed = ''

    # rb // read binary
    with open(file_to_transcript, mode='rb') as file_audio:
        response = speech_transcription.recognize(audio=file_audio, content_type='audio/mp3')
        logger.info(response.result['results'])
        for text in response.result['results']:
            text_transcribed += f" {text['alternatives'][0]['transcript']} |"
    return text_transcribed


def translate_text(text: [str]):
    authenticator = IAMAuthenticator(apikey=pass_api_translate)
    language_translator = LanguageTranslatorV3(
        version=version_api_translate,
        authenticator=authenticator
    )

    language_translator.set_service_url(api_translate)

    # EN to ES
    translation_response = language_translator.translate(text=text, model_id='en-es')
    translation_text = translation_response.get_result()
    logger.info(translation_text)
    return translation_text['translations'][0]['translation']



if __name__ == '__main__':
    file_to_transcript = './files/test.mp3'
    text_audio = transcript_audio(file_to_transcript)
    text_translated = translate_text([text_audio])
    print(text_translated)
