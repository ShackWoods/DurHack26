import pygame
from tkinter import *

class Speaker:
    def __init__(self):
        self.image = None
        self.times = []
        self.talking = False
        self.current = 0

    def set_position(self, x: int, y: int):
        self.pos = (x, y)

    def set_image(self, image: pygame.image):
        self.image = image

    def extend_times(self, start: int, end: int):
        self.times.append(range(start, end))

def translate_miliseconds(raw_time):
    hours = int(raw_time[0:2])
    mins = int(raw_time[3:5])
    secs = int(raw_time[6:8])
    milsecs = int(raw_time[9:])
    total = milsecs + 1000*secs + 60*1000*mins +60*60*1000*hours
    return total

# Our constants
SCREEN_SIZE = (1480, 900)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
FPS = 30       



speakers = {} # Dictionary of guys
with open("TRANSCRIPT_TEMP.txt", "r") as f: # Opens file
    lines = f.read().split("\n")
    for l in range(0, len(lines), 3): # Reads every third line cos of the format
        # Splits into to when speech starts, ends and speaker name
        line = lines[l]
        parts = line.split(" ")
        start, end = parts[0], parts[2]
        speaker_id = " ".join(parts[3:])[1:-1] 

        # Puts time range into speaker's list
        if(speaker_id not in speakers):
            speakers[speaker_id] = Speaker()
        speakers[speaker_id].extend_times(translate_miliseconds(start), translate_miliseconds(end))

# Load images
if(len(speakers) > 2): # We aren't handling this rn
    raise Exception("Nuh uh, too many people")
guys = ["olivia.png","oliver.png"]
for i, speaker in enumerate(speakers):
    popper = pygame.image.load(f"{guys[i]}").convert_alpha() # Load the image
    speakers[speaker].set_image(popper) # Set the image
    speakers[speaker].set_position(i * popper.get_width(), SCREEN_SIZE[1] - popper.get_height()) # Set the position

talking_mouth = pygame.image.load("talking_mouth.png").convert_alpha()
silent_mouth = pygame.image.load("silent_mouth.png").convert_alpha()



# The main loop
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
        for i in range(len(speaker.times)):

            # If between start and end for speakers[id] that speaker is talking
            if time_current in speaker.times[i][0]:
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
    if(time_current >= 60000):
        running = False
pygame.quit()