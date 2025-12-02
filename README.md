## AI Speak‑Think‑Play Tool 0.1.0  
*A lightweight utility for interacting with an LLM via audio (or a text prompt) and receiving spoken responses.*

---

### What It Does
- **Transcribes** spoken input (audio file) with a local Speech‑to‑Text (STT) model (privacy‑first for your voice).  
- Sends the transcription to a Gemini LLM.  
- Returns the LLM’s answer as **speech** using Text‑to‑Speech (TTS).  

> Ideal for polishing pronunciation in foreign languages, but flexible enough for any audio‑driven workflow.



## Quick Presentation

### Audio input `hi.wav`

<audio controls>
  <source src="./Samples/hi.wav" type="audio/wav">
  Your browser does not support the audio element.
</audio>

#### Transcription:
`Hi, tell me about your day.`

#### Command:
```bash
uv run main.py --verbose "Samples/hi.wav"
```
#### Logs
```
Initializing LLM client
Initializing STT client (Whisper)
Loading audio from 'Samples/hi.wav' and finding language
Detected language: en
Decoding Audio

---Audio Transcript---
Hi, tell me about your day.
------------

Initializing TTS client
Setting LLM client with model and getting response (gemini-2.0-flash)

---Response---
Hello! My day has been quite good so far. I've been helping many students with their English, just like I'm doing with you now. How about you, how was your day?

---------


===COST===
Prompt tokens: 119 --- Cost: 0.00001785 $
Response tokens: 42 --- Cost: 0.00002520 $
===$$$===

Setting TTS client with model (gemini-2.5-flash-lite-preview-tts - Enceladus) and sending request.
Got response, saving it to file

===COST===
Text tokens: 224 --- Cost: 0.000112 $
Audio tokens: 247 --- Cost: 0.002470 $
===$$$===

Audio content written to file: response.mp3
```

#### Audio Output 

<audio controls>
  <source src="./Samples/example_response2.mp3" type="audio/mpeg">
  Your browser does not support the video tag.
</audio>

#### Transcription:
`Hello! My day has been quite good so far. I've been helping many students with their English, just like I'm doing with you now. How about you, how was your day?`

### Prerequisites  

| Item | How to obtain |
|------|----------------|
| **Vertex AI API key** | Create a Vertex AI project in Google Cloud, enable the API, then copy the key into a `.env` file as `VERTEX_AI_API_KEY`. |
| **OAuth2 service‑account JSON** | In the same Google Cloud project, enable the **Text‑to‑Speech** API, create a service‑account key, and store the file path in `.env` as `SECRET_JSON_FILEPATH`. |

> **Note:** This is a learning / testing project. You are fully responsible for any costs (e.g., token usage, Google Cloud quotas) incurred by running the code.

---

## Installation  


### Clone the repo (if you haven’t already)

```bash
git clone https://github.com/ArchBober/AI-Speak-Think-Play-Tool.git
cd AI-Speak-Think-Play-Tool
```
### Install dependencies with uv (recommended)
```bash
uv venv
source .venv/bin/activate # on windows can be different
uv sync   # reads pyproject.toml
```

### Running the Tool  

```bash
uv run main.py [options] <input-audio-filepath>
uv run main.py [options] --prompt "<your prompt text>"
```
#### Options  

| Flag | Description |
|------|-------------|
| `--help` | Show the help text (this document). |
| `--prompt "<text>"` | Bypass STT and feed your own prompt directly to the LLM. |
| `--verbose` | Enable detailed logging and extra CLI output. |

**Examples**

```bash
# Normal usage – record from microphone or load an audio file
uv run main.py "audiofile.mp3"

# Supply a custom prompt instead of transcribing audio
uv run main.py --prompt "Explain quantum entanglement in plain English."

# Get verbose output for debugging
uv run main.py "audiofile.mp3" --verbose
```
### How It Works (high‑level)

1. **Capture audio** (for now only file).  
2. **Local STT** → produces a text transcript.  
3. **Send transcript** to a Gemini model (via Vertex AI).  
4. **Receive LLM response** (text).  
5. **TTS** → synthesize the response as audio and play it back.

---

## Configuration Constants

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `OUTPUT_AUDIO_FILEPATH` | `"response.mp3"` | Path (relative or absolute) where the synthesized speech audio will be saved after the TTS step. |
| `LANGUAGE` | `"en-US"` | BCP‑47 language tag used by the STT and TTS services (e.g., `en-US`, `es-ES`, `fr-FR`). |
| `LANGUAGE_LVL` | `"B1"` | Target proficiency level for the learner (A1‑B2 range). This value is injected into the LLM prompt to adapt the difficulty of the conversation. |
| `SPEAKING_RATE` | `1.2` | Speed multiplier for the generated voice. `1.0` is the default; acceptable range is roughly `0.5` (slow) → `2.0` (fast). |
| `STT_MODEL` | `"turbo"` | Identifier of the Whisper‑style speech‑to‑text model. Options include:<br>• `tiny` (≈ 1 GB VRAM)<br>• `base` (≈ 1 GB VRAM)<br>• `small` (≈ 2 GB VRAM)<br>• `medium` (≈ 5 GB VRAM)<br>• `large` (≈ 10 GB VRAM)<br>• `turbo` (≈ 6 GB VRAM, fastest inference). |
| `LLM_MODEL` | `"gemini-2.0-flash"` | The generative‑AI model used for the dialogue. Gemini‑2.0‑Flash offers a good balance of speed and quality for conversational tasks. |
| `TTS_MODEL` | `"gemini-2.5-flash-lite-preview-tts"` | The text‑to‑speech model that produces the audio response. The *lite* preview is optimized for lower latency and cost. |
| `TTS_VOICE` | `"Enceladus"` | Named voice preset supplied by the TTS model. Different voices have distinct timbres and accents; choose the one that best fits a language‑teacher persona. |
| `LLM_PROMPT` | *(see below)* | System prompt fed to the LLM. It sets the role (“language teacher”), tone (simple vocabulary, short answers), student proficiency (`{LANGUAGE_LVL}`), and name (`Mark Spencer`). The prompt also encourages ending replies with a question to keep the conversation flowing. |
| `TTS_PROMPT` | `"As a teacher of en_US language talk with calm and polite voice."` | Optional instruction for the TTS engine to shape prosody (calm, polite) and reinforce the teaching persona. |
| ~~`MAX_CHARS`~~ | ~~`10000`~~ | `NOT IMPLEMENTED!` ~~Upper limit on the number of characters that can be sent to the LLM in a single request. Prevents oversized payloads that could exceed API limits.~~ |
| `TTS_AUDIO_TOKEN_PRICE` | `10` | Cost (in your chosen currency unit) per **audio token** generated by the TTS model. Useful for budgeting and cost‑tracking scripts. Must be adjusted by user (check pricing page for each model) |
| `TTS_TEXT_TOKEN_PRICE` | `0.5` | Cost per **text token** processed by the TTS model (the input text length). Must be adjusted by user (check pricing page for each model) |
| `LLM_INPUT_TOKEN_PRICE` | `0.15` | Cost per **input token** sent to the LLM. Must be adjusted by user (check pricing page for each model) |
| `LLM_OUTPUT_TOKEN_PRICE` | `0.6` | Cost per **output token** returned by the LLM. Must be adjusted by user (check pricing page for each model) |

### Example of the `LLM_PROMPT` and `TTS_PROMPT`

```python
LLM_PROMPT = f"""
You are {LANGUAGE} teacher that help with basic difficulties of learning that language. 
Your main goal is to talk to student and use not too many hard words. 
Students are expected to be on level A1 up to B2 in that language. 
Your today student is expected to be on {LANGUAGE_LVL} language profficiency. 
Your name is Mark Spencer but tell your name only when asked. 
Also try to keep responses short and straight to the point. 
If possible try to end sentences with questions for student to keep conversation.
"""

TTS_PROMPT=f"""As a teacher of {LANGUAGE} language talk with calm and polite voice."""
```


## Available models and languages for STT (Whisper OpenAI)

There are six model sizes, four with English-only versions, offering speed and accuracy tradeoffs.
Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model.
The relative speeds below are measured by transcribing English speech on a A100, and the real-world speed may vary significantly depending on many factors including the language, the speaking speed, and the available hardware.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~10x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~7x       |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~4x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
| turbo  |   809 M    |        N/A         |      `turbo`       |     ~6 GB     |      ~8x       |

---

### Sources worth peeking

| Topic | Resource | URL |
|-------|----------|-----|
| **Google Vertex AI Overview** | Official product page | https://cloud.google.com/vertex-ai |
| **Google Vertex AI Model Garden** | Catalog of pre‑trained models (including Gemini, PaLM, Imagen, etc.) | https://cloud.google.com/model-garden?hl=en|
| **Google Vertex AI Model Garden** | Catalog of pre‑trained models (including Gemini, PaLM, Imagen, etc.) | https://cloud.google.com/model-garden?hl=en|
| **Whisper OpenAI** | STT local models | https://github.com/openai/whisper |
| **Text‑to‑Speech (TTS) API** | Documentation for Google Cloud TTS, supported voices & formats | https://cloud.google.com/text-to-speech/docs |
| **Speech‑to‑Text (STT) API** | Docs for streaming and batch speech recognition | https://cloud.google.com/speech-to-text/docs |
| **Authentication (Service Accounts & OAuth2)** | How to create and use service‑account keys for Vertex AI | https://cloud.google.com/docs/authentication/production |
| **Quota & Billing for Vertex AI** | Information on token usage, request limits, and cost estimation | https://cloud.google.com/vertex-ai/pricing |
| **Vertex AI Samples & Tutorials** | End‑to‑end notebooks and code snippets for common use‑cases | https://github.com/GoogleCloudPlatform/vertex-ai-samples |
| **Google Generative AI Playground** (interactive demo of Gemini models) | Quick way to test prompts and see model capabilities | https://makersuite.google.com/app/apikey |
| **Security & Compliance** | Data protection, encryption, and compliance certifications for Vertex AI | https://cloud.google.com/security/compliance |


### Disclaimer  

- This repository is provided **as‑is** for experimentation and learning.  
- The author assumes **no liability** for misuse, unexpected costs, or service restrictions arising from running the code.  
- By using or modifying the tool you accept full responsibility for any consequences (e.g., high token consumption, hitting Google Cloud limits, etc.).

--- 

Feel free to tweak the code, swap out the Gemini models, or integrate your own STT/TTS engines! 🎤🗣️✨