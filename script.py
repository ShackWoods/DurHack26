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



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
FPS = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()