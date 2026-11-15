from syllabify import syllabify
import json
import re

#mouthabet
mouthabet = {"AA": 0,
             "AE": 3,
             "AH": 6,
             "AO": 3,
             "AW": 4,
             "AX": 3,
             "AXR": 10,
             "AY": 3,
             "EH": 3,
             "EY": 3,
             "IH": 3,
             "IX": 3,
             "IY": 5,
             "OW": 0,
             "OY": 0,
             "UH": 6,
             "UW": 0,
             "UX": 4,
             "B": 2,
             "CH": 7,
             "D": 1,
             "DH": 11,
             "DX": 1,
             "EL": 8,
             "EM": 2,
             "ER": 10,
             "EN": 1,
             "F": 9,
             "G": 1,
             "HH": 6,
             "H": 6,
             "JH": 7,
             "K": 1,
             "L": 8,
             "M": 2,
             "N": 1,
             "NX": 5,
             "NG": 5,
             "NX": 11,
             "P": 2,
             "Q": 4,
             "R": 10,
             "S": 1,
             "SH": 7,
             "T": 1,
             "TH": 11,
             "V": 9,
             "W": 4,
             "WH": 4,
             "Y": 1,
             "Z": 1,
             "ZH": 1
             }

def syllablize(filename: str) -> list:
    global mouthabet
    
    words = []
    with open(f"Source/{filename}", "r") as f:
        data = json.load(f)
        raw_words = data["segments"]["words"]
        for word_dict in raw_words:
            word = word_dict["text"]

            while word[-1] in [".", ",", ":", ";"]: # Remove ending punctuation
                word = word[:-1]
            syllables = syllabify(word)

            if(syllables is None):
                 continue

            temp = re.sub(r'\{.*?\}','', str(syllables)) # Separate to get the onset, nucleus and coda from each word
            # Splits into parts and removes the numbers from the onset, nucleus and coda
            parts = (re.sub(r'\d+', '',temp)).split(" ") # Using google search: https://www.geeksforgeeks.org/python/python-ways-to-remove-numeric-digits-from-given-string/

            # Assign a mouths for the word
            mouths = []
            for part in parts:
                if(part != ""):
                    mouths.append(mouthabet[part])
            word_dict["text"] = mouths
            words.append(word_dict)
    return words #list of dictionaries. each dictionary is the list of mouths, start and end and speaker id for each word