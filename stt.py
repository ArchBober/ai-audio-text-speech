import whisper
from config import STT_MODEL

def stt(audio_filepath: str, verbose: bool = False) -> str:
    # ctrl+c ctrl+v from wshiper readme but work perfectly
    stt_model = whisper.load_model(STT_MODEL)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("Samples/message_accepted.wav")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=stt_model.dims.n_mels).to(stt_model.device)

    # detect the spoken language
    # TODO add loop if lang != EN or enforce EN transciption
    _, probs = stt_model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result_audio_trans = whisper.decode(stt_model, mel, options)

    # print the recognized text
    if verbose:
        print(result_audio_trans.text)

    return result_audio_trans.text