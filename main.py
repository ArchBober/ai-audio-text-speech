from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, Modality
from google.api_core.client_options import ClientOptions
from google.cloud import texttospeech
from google.oauth2 import service_account

import sys
import os

from stt import stt
from llm import llm
from config import LLM_PROMPT, TTS_PROMPT

from dotenv import load_dotenv

print("got init")

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


    transcription = stt("Samples/message_accepted.wav", verbose)

    client = genai.Client(
            vertexai=True, api_key=api_key,
        )
    
    clientoptions = ClientOptions(api_key=api_key)

    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    SERVICE_ACCOUNT_FILE = "secret.json"

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE
    )

    ttsclient = texttospeech.TextToSpeechClient(credentials=creds)

    synthesis_input = texttospeech.SynthesisInput(text=transcription, prompt=TTS_PROMPT)

    print("TTS Client initialized. Sending request...")

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="Charon",  # Example voice, adjust as needed
        model_name="gemini-2.5-pro-tts"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = ttsclient.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

    with open("response.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file: response.mp3")

    # try:
    #     response = client.models.generate_content(
    #         model="gemini-2.0-flash", 
    #         contents=result_audio_trans.text
    #     )
        
    #     print("\n--- Response ---")
    #     print(response.text)
    #     print("----------------")

    #     if verbose:
    #         print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #         print("Response tokens:", response.usage_metadata.candidates_token_count)
        

    # except Exception as e:
    #     print(f"\nError: {e}")


    # try:
    #     response = client.models.generate_content(
    #         model="en-US-Chirp3-HD-Charon",
    #         contents="Generate sound of water.",
    #         config=GenerateContentConfig(
    #             response_modalities=[Modality.AUDIO],
    #         ),
    #     )
    #     for part in response.candidates[0].content.parts:
    #         if part.text:
    #             print(part.text)
    #         elif part.inline_data:
    #             print(f"some bytes {len(part.inline_data)}")
    #     print("\n--- Response ---")
    #     print(response)
    #     print("----------------")

    #     if verbose:
    #         print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #         print("Response tokens:", response.usage_metadata.candidates_token_count)
        
    # except Exception as e:
    #     print(f"\nError: {e}")



if __name__ == "__main__":
    main()