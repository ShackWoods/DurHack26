import pygame
import random

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

def load_and_scale(file: str, scalar: int) -> pygame.Surface:
    image = pygame.image.load(f"Images/{file}").convert_alpha()
    return pygame.transform.smoothscale_by(image, scalar)

# Our constants
SCREEN_SIZE = (1480, 810)
guys = ["olivia.png","oliver.png"]
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
FPS = 30      

 
#Load the transcript into the guys
speakers = {} # Dictionary of guys
with open("Source/TRANSCRIPT_TEMP.txt", "r") as f: # Opens file
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

# ERROR - NO SPEAKER
if(len(speakers) == 0):
    raise Exception("No speakers detected, try another audio clip")

# Determine how the guys need scaling
rows = 0
while 2 * rows * rows < len(speakers):
    rows += 1
scalar = 1 / rows
cols = 2 * rows
BLOCK_SIZE = (SCREEN_SIZE[0] / cols, SCREEN_SIZE[1] / rows)
rows -= 1

# Load images
talking_mouth = load_and_scale("talking_mouth.png", scalar)
silent_mouth = load_and_scale("silent_mouth.png", scalar)

poppers = [load_and_scale(guy, scalar) for guy in guys]
for i, speaker in enumerate(speakers):
    popper = poppers[random.randint(0,1)] # Choose a random guy
    speakers[speaker].set_image(popper) # Set the image
    x = BLOCK_SIZE[0] * (i % cols) # x on the grid of guys
    y = BLOCK_SIZE[1] * (rows - (i // cols)) # y on the grid of guys
    speakers[speaker].set_position(x, y) # Set the position



# The main loop
pygame.mixer.init()
pygame.mixer.music.load("Source/TRANSCRIPT_SOURCE.mp3")
pygame.mixer.music.play()
time_current = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: #EARLY END CONDITION
            running = False
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    # Make them pop
    for id in speakers: # For each speaker
        speaker = speakers[id]
        
        speaker.talking = False
        for i in range(len(speaker.times)): # Go through each time range
            if time_current in speaker.times[i]: # If between start and end for speakers[id] that speaker is talking
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
pygame.display.quit()
pygame.quit()