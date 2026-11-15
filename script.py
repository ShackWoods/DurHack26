import pygame
import json

class Speaker:
    def __init__(self):
        self.image = None
        self.script = []
        self.talking = False

    def set_position(self, x: int, y: int):
        self.pos = (x, y)

    def set_image(self, image: pygame.image):
        self.image = image

    def extend_times(self, start: int, end: int, word: str):
        self.script.append((range(start, end), word))

# Our constants
SCREEN_SIZE = (1480, 900)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
FPS = 30       

speakers = {} # Dictionary of guys
with open("Source/transcript.json", "r") as f:
    data = json.load(f)
    for word in data["segments"]["words"]:
        text = word["text"]
        start, end = word["start"], word["end"]
        speaker_id = word["speaker_id"]
        if(speaker_id not in speakers):
            speakers[speaker_id] = Speaker()
        speakers[speaker_id].extend_times(int(start*1000), int(end*1000), text)
        


# Load images
if(len(speakers) > 2): # We aren't handling this rn
    raise Exception("Nuh uh, too many people")
guys = ["olivia.png","oliver.png"]
for i, speaker in enumerate(speakers):
    popper = pygame.image.load(f"Images/{guys[i]}").convert_alpha() # Load the image
    speakers[speaker].set_image(popper) # Set the image
    speakers[speaker].set_position(i * popper.get_width(), SCREEN_SIZE[1] - popper.get_height()) # Set the position

talking_mouth = pygame.image.load("Images/talking_mouth.png").convert_alpha()
silent_mouth = pygame.image.load("Images/silent_mouth.png").convert_alpha()



# The main loop
pygame.mixer.init()
pygame.mixer.music.load("Source/TRANSCRIPT_SOURCE.mp3")
pygame.mixer.music.play()
time_current = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    # Make them pop
    for id in speakers: # For each speaker
        speaker = speakers[id]

        # Go through each time range
        speaker.talking = False
        for i in range(len(speaker.script)):

            # If between start and end for speakers[id] that speaker is talking
            if time_current in speaker.script[i][0]:
                speaker.talking = True
        screen.blit(speaker.image, speaker.pos)
        if(speaker.talking):
            screen.blit(talking_mouth, speaker.pos)
        else:
            screen.blit(silent_mouth, speaker.pos)

    pygame.display.flip() # Draw to screen
    dt = clock.tick(FPS) # How many milliseconds have passed
    time_current += dt

    # End condition
    if(not pygame.mixer.music.get_busy()):
        running = False
pygame.mixer.music.stop()
pygame.quit()