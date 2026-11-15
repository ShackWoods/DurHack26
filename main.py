from transcriber import transcribe
from syllablizer import syllablize
#from visualizer import visualize
import json

def test_file_exists(filename) -> bool:
    try:
        f = open("Source/" + filename)
        f.close()
    except:
        return False
    return True

def run() -> str:
    with open(f"Source/settings.json", "r") as f:
        settings = json.load(f)

    audio_filename = ""
    transcript_filename = ""
    try:
        audio_filename = settings["audio_source"]
    except:
        return "NO AUDIO SOURCE SUPPLIED"
    
    try:
        transcript_filename = settings["transcript_source"]
    except:
        return "NO TRANSCRIPT SUPPLIED - YOU MAY LEAVE THIS FIELD AS \"\""

    # Ensure audio track exists
    if(not test_file_exists(audio_filename)):
        return f"Audio source: '{settings["audio_source"]} does not exist in Source/"

    # Transcribe
    if(transcript_filename is None or transcript_filename == ""): # Create a transcript
        transcribe(audio_filename)
        transcript_filename = "transcript.json"
    # Ensure transcript is valid
    if(transcript_filename[-5:] != ".json"):
        return "Wrong Extension: " + transcript_filename
    if(not test_file_exists(transcript_filename)):
        return "Transcript not found: " + transcript_filename

    # Syllabalize
    word_list = syllablize(transcript_filename)
    for w in word_list:
        print(w)

    # Visualize
    return "Success :D"

if __name__ == "__main__":
    print(run())