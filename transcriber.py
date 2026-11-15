# Stolen directly from https://elevenlabs.io/docs/eleven-api/guides/cookbooks/speech-to-text
import os
from dotenv import load_dotenv
from io import BytesIO
from elevenlabs.client import ElevenLabs
import json

# Calls the ElevenLabs API to transcribe the supplied mp3
def transcribe(filename:str) -> None:
    load_dotenv()
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    data = None
    with open(f"Source/{filename}", "rb") as file:
        data = file.read()
    audio_data = BytesIO(data)

    transcription = elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v3", # Model to use
        tag_audio_events=True, # Tag audio events like laughter, applause, etc.
        language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
        diarize=True, # Whether to annotate who is speaking
    )

    words = []
    for word in transcription.words:
        if(word.type != "word"):
            continue
        word_info = {"text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "speaker_id": word.speaker_id}
        words.append(word_info)

    segments = {"words": words}
    data = {"segments": segments}
    with open("Source/transcript.json", "w") as f:
        json.dump(data, f)