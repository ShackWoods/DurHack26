import pygame
from tkinter import *

# pygame setup
SCREEN_SIZE = (1480, 900)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
FPS = 30

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

    def extend_times(self, start, end):
        self.times.append((start, end))

speakers = {} #dictionary of guys
with open("TRANSCRIPT_TEMP.txt", "r") as f: #opens file
    lines = f.read().split("\n")
    for l in range(0, len(lines), 3): #reads every third line cos of the format
        line = lines[l]
        parts = line.split(" ")
        start, end = parts[0], parts[2]
        #splits into to when speech starts, ends and speaker name
        speaker_id = " ".join(parts[3:])[1:-1] 

        if(speaker_id not in speakers):
            speakers[speaker_id] = Speaker() #puts into speaker's list
        speakers[speaker_id].extend_times(start, end)

if(len(speakers) > 2):
    raise Exception("Nuh uh, too many people")
guys = ["olivia.jpeg","oliver.jpeg"]
for i, speaker in enumerate(speakers):
    popper = pygame.image.load(f"{guys[i]}").convert_alpha()
    popper.set_colorkey((0,255,85))
    speakers[speaker].set_image(popper)
    speakers[speaker].set_position(i * popper.get_width(), SCREEN_SIZE[1] - popper.get_height())

talking_mouth = pygame.image.load("talking_mouth.jpeg").convert_alpha()
silent_mouth = pygame.image.load("silent_mouth.jpeg").convert_alpha()
talking_mouth.set_colorkey((0,255,85))
silent_mouth.set_colorkey((0,255,85))

time_current = 0

def translate_miliseconds(time):
    hours = int(time[0:2])
    mins = int(time[3:5])
    secs = int(time[6:8])
    milsecs = int(time[9:])
    total = milsecs + 1000*secs + 60*1000*mins +60*60*1000*hours
    return total

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    #sets and unsets the person talking
    for id in speakers:
        speaker = speakers[id]
        #which speaker is speaker at the current time
        speaker.talking = False
        for i in range(len(speaker.times)):
            #convert to milliseconds
            start = translate_miliseconds(speaker.times[i][0])
            end = translate_miliseconds(speaker.times[i][1])
            #if between start and end for speakers[id] that speaker is talking
            if time_current >= start and time_current <= end:
                speaker.talking = True
        screen.blit(speakers[speaker].image, speakers[speaker].pos)
        if(speakers[speaker].talking):
            screen.blit(talking_mouth, speakers[speaker].pos)
        else:
            screen.blit(silent_mouth, speakers[speaker].pos)

    
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(FPS) #how many milliseconds have passed
    time_current += dt

    if(time_current >= 60000):
        running = False
pygame.quit()