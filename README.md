# POPPERS
An app to animate mouths from an input audio track.

## How to use
Place an mp3 file and (optionally) a transcript JSON in the Source folder.  
Esnure settings.json is correctly filled in.

The program will automatically follow this pipeline:  
- Call ElevenLabs to transcribe the file if not JSON supplied
- Convert words to ARPABET syllables
- Visualize it all with "Poppers"

## Dependencies
pygame  
syllabify  
elevenlabs  
dotenv

You will need an ElevenLabs API key in a .env file.