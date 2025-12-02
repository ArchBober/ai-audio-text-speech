from google.oauth2 import service_account
from google import genai
from google.cloud import texttospeech

import sys
import os

from stt import stt
from llm import llm
from tts import tts
from config import OUTPUT_AUDIO_FILEPATH
from help_description import HELP_DESCRIPTION

from dotenv import load_dotenv

import warnings

# ignore regex warning from pydub
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

    if "--help" in sys.argv:
        print(HELP_DESCRIPTION)
        sys.exit(0)

    verbose = "--verbose" in sys.argv
    prompt = "--prompt" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if prompt:
        if len(args[0].strip()) < 1:
            print("Prompt too short. Exiting.")
            sys.exit(1)

    if not args:
        # TODO implement args
        print("Did not get necessary arguments.\n")
        print(HELP_DESCRIPTION)
        sys.exit(1)

    if verbose:
        print("Initializing LLM client")

    client_llm = genai.Client(
        vertexai=True, api_key=api_key
    )

    if prompt:
        if verbose:
            print("User used flag --prompt. Overriding TTS transcription")
            
        transcription = args[0]
    else:
        transcription = stt(args[0], verbose)

    if verbose:
        print("Initializing TTS client")

    client_tts = texttospeech.TextToSpeechClient(
        credentials=service_account.Credentials.from_service_account_file(
            secret_json_filepath
        )
    )

    llm_response = llm(client_llm, transcription, verbose)
    tts(client_tts, llm_response, OUTPUT_AUDIO_FILEPATH, verbose)



if __name__ == "__main__":
    main()