from google.cloud import texttospeech

from config import TTS_MODEL, TTS_PROMPT, TTS_VOICE, LANGUAGE

def tts(client_tts: texttospeech.TextToSpeechClient, input_content: str, save_filepath: str = "sample_output.mp3", verbose: bool = False) -> None:
    try:
        if verbose:
            print(f"Setting TTS client with model ({TTS_MODEL} - {TTS_VOICE}) and sending request.")

        synthesis_input = texttospeech.SynthesisInput(text=input_content, prompt=TTS_PROMPT)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=LANGUAGE,
            name=TTS_VOICE,
            model_name=TTS_MODEL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client_tts.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        if verbose:
            print("Got response, saving it to file")

        with open(save_filepath, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to file: {save_filepath}")
    
    except Exception as e:
        print(f"\nError: {e}")
    
    return