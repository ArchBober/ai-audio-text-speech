from google.oauth2 import service_account
from google import genai
from google.cloud import texttospeech

import sys
import os

from stt import stt
from llm import llm
from tts import tts

from dotenv import load_dotenv

import warnings

warnings.filterwarnings(
    action="ignore",      
    category=UserWarning,          
    module=r"^pydub\.",           
    message=r".*"                 
)

def main():
    load_dotenv()

    api_key = os.environ.get("VERTEX_AI_API_KEY")
    secret_json_filepath = os.environ.get("SECRET_JSON_FILEPATH")


    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        # TODO implement args
        print("Audio-Text-Speach AI - no args")
        sys.exit(1)

    if verbose:
        print("Initializing LLM client")

    client_llm = genai.Client(
        vertexai=True, api_key=api_key
    )

    if verbose:
        print("Initializing TTS client")

    client_tts = texttospeech.TextToSpeechClient(
        credentials=service_account.Credentials.from_service_account_file(
            secret_json_filepath
        )
    )

    transcription = stt("Samples/france.wav", verbose)
    llm_response = llm(client_llm, transcription, verbose)
    tts(client_tts, llm_response, "response.mp3", verbose)



if __name__ == "__main__":
    main()