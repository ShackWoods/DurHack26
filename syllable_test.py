from syllabify import syllabify
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

with open("Source/TRANSCRIPT_TEMP.txt", "r") as f: # Opens file
    lines = f.read().split("\n")#

    #total mouth sequence for video
    total_mouths =[]
    for l in range(1, len(lines), 3): # Reads every third line cos of the format
        # Splits into to when speech starts, ends and speaker name
        line = lines[l]
        words = line.split(" ")
        print(words)
        mouths_per_line = []

        for word in words:
            try:
                k = syllabify(word)
            except:
                k = syllabify(word[:-1]) #cos doesnt like fullstop
            print(k, type(k))
            if k != None: 
                    #separate to get the onset, nucleus and coda from each word
                    temp = re.sub(r'\{.*?\}','', str(k))
                    print(temp)
                    
                    #splits into parts and removes the numbers from the onset, nucleus and coda
                    parts = (re.sub(r'\d+', '',temp)).split(" ")  #using google search: https://www.geeksforgeeks.org/python/python-ways-to-remove-numeric-digits-from-given-string/
                    print(parts)
                    #remove any spaces
                    for part in parts:
                         if part == "":
                              parts.remove(part)
            
                    #assign a mouths for the word
                    mouths = []
                    for part in parts:
                        mouths.append(mouthabet[part])
            
                    print(mouths)
                    mouths_per_line.extend(mouths) #add the mouths for the word to the mouths for the line
        print(mouths_per_line)            
        total_mouths.append(mouths_per_line) #add to the total mouths for the script

print(total_mouths)
           
