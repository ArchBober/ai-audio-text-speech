from google import genai
from google.genai import types
# from google.cloud.speech_v2 import SpeechClient
# from google.cloud.speech_v2.types import cloud_speech

import sys
import os

from dotenv import load_dotenv

print("got init")

PROJECT_ID = os.getenv("PROJECT_ID")

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        # TODO implement args
        print("Audio-Text-Speach AI - no args")
        sys.exit(1)

    api_key = os.environ.get("YOUR_VERTEX_AI_API_KEY")
    project_id = os.environ.get("PROJECT_ID")
    project_location = os.environ.get("PROJECT_LOCATION")

    print("got env")

    client = genai.Client(
        vertexai=True, api_key=api_key,
    )

    print("Client initialized. Sending request...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Are you online? Reply with 'Connection Successful'."
        )
        
        print("\n--- Response ---")
        print(response.text)
        print("----------------")

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
    except Exception as e:
        print(f"\nError: {e}")

    print("TESTING READ AUDIO FILE")

    with open("FreeSamplesPixabay/nowwhat-96488.mp3", "rb") as f:
        audio_content = f.read()

    print("AUDIO FILE OPENED")
    print("TEST SPEECH CLIENT")

    # speechclient = SpeechClient()
    # model =genai.GenerativeModel("speech_to_text")

    print("SPEECH CLIENT CREATED")
    print("SPEECH CLIENT - SETTING CONFIG")

    # config = cloud_speech.RecognitionConfig(
    #     auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    #     language_codes=["en-UK"],
    #     model="long",
    # )

    print("SPEECH CLIENT CONFIG CREATED")

    print("REQUESTING TRANSCRIPTION RECOGNIZER")

    # request = cloud_speech.RecognizeRequest(
    #     config=config,
    #     content=audio_content,
    # )

    print("SET TRANSCRIPTION RECOGNIZER")

    print("GETTING RESPONSE")

    # try:
    #     response = client.recognize(request=request)
        
    #     print("\n--- Response ---")
    #     for result in response.results:
    #         print(f"Transcript: {result.alternatives[0].transcript}")
    #     print("----------------")

    #     # if verbose:
    #     #     print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #     #     print("Response tokens:", response.usage_metadata.candidates_token_count)
        
    # except Exception as e:
    #     print(f"\nError: {e}")


if __name__ == "__main__":
    main()