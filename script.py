import pygame
from tkinter import *

class Speaker:
    def __init__(self):
        self.image = None
        self.times = []
        self.talking = False
        self.current = 0

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

time_current = 0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
FPS = 30

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
        print("at",time_current,":",speaker.talking)

    
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(FPS) #how many milliseconds have passed
    time_current += dt

    if(time_current >= 60000):
        running = False
pygame.quit()