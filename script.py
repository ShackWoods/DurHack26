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

speakers = {}
with open("TRANSCRIPT_TEMP.txt", "r") as f:
    lines = f.read().split("\n")
    for l in range(0, len(lines), 3):
        line = lines[l]
        parts = line.split(" ")
        start, end = parts[0], parts[2]
        speaker_id = " ".join(parts[3:])[1:-1]

        if(speaker_id not in speakers):
            speakers[speaker_id] = Speaker()
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

import random
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    for speaker in speakers:
        if(random.randint(0,60) == 5):
            speakers[speaker].talking = not speakers[speaker].talking
        screen.blit(speakers[speaker].image, speakers[speaker].pos)
        if(speakers[speaker].talking):
            screen.blit(talking_mouth, speakers[speaker].pos)
        else:
            screen.blit(silent_mouth, speakers[speaker].pos)


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()