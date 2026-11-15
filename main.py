from transcriber import transcribe
from syllablizer import syllablize
#from visualizer import visualize

def test_file_exists(filename) -> bool:
    try:
        f = open("Source/" + filename)
        f.close()
    except:
        return False
    return True

def run() -> str:
    transcription_required = input("Do you have a transcript already? (y or n)\n") == "n"
    filename = input("What is the name of your file (with file extension)\n")

    if(not test_file_exists):
        return f"'{filename}' is invalid, please ensure the spelling is correct and that file exists in Source/"

    # Transcribe
    transcript_filename = ""
    if(transcription_required):
        transcribe(filename)
        transcript_filename = "transcript.json"
    else:
        transcript_filename = input("What is the name of your transcript (must be a JSON)\n")
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