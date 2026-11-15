import pygame
import random
import glob

class Speaker:
    def __init__(self):
        self.image = None
        self.script = []
        self.mouth = -1

    def set_position(self, x: int, y: int):
        self.pos = (x, y)

    def set_image(self, image: pygame.image):
        self.image = image

    def extend_times(self, start: int, end: int, word: str):
        self.script.append((range(start, end), word))


def load_and_scale(file: str, scalar = 1) -> pygame.Surface:
    image = pygame.image.load(file).convert_alpha()
    #scales and then returns it
    return pygame.transform.smoothscale_by(image, scalar)

def visualize(audio_filename: str, words: list, FPS: int, custom_images: bool) -> str:
    # Our constants
    SCREEN_SIZE = (1480, 810)
    guys = ["olivia.png","oliver.png"]
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True

    image_path = "Images"
    if(not custom_images):
        image_path += "/default"
        guys = ["olivia.png","oliver.png"]
    else:
        guys = [f[15:] for f in glob.glob("Images/Poppers/*.png")]
        if(len(guys) == 0):
            return "No custom poppers found"

    speakers = {} # Dictionary of guys
    for word in words:
        text = word["text"]
        start, end = word["start"], word["end"]
        speaker_id = word["speaker_id"]
        if(speaker_id not in speakers):
            speakers[speaker_id] = Speaker()
        speakers[speaker_id].extend_times(int(start*1000), int(end*1000), text)


            
    # ERROR - NO SPEAKER
    if(len(speakers) == 0):
        return "ERROR: No speakers detected, try another audio clip"

    # Determine how the guys need scaling
    rows = 0
    while 2 * rows * rows < len(speakers):
        rows += 1
    scalar = 1 / rows
    cols = 2 * rows
    BLOCK_SIZE = (SCREEN_SIZE[0] / cols, SCREEN_SIZE[1] / rows)
    rows -= 1

    # Load images
    silent_mouth = load_and_scale(f"{image_path}/Mouths/silent_mouth.png", scalar)
    #add the mouth options
    mouth_images = []
    #at position 0 is the 0 mouth, at 1 is the 1 mouth
    for i in range(0,12):
        try:
            img = load_and_scale(f"{image_path}/Mouths/{i}.png",scalar)
        except:
            return "Either mouth images are wrong, or some mouths are missing"
        mouth_images.append(img)
    #at the end of list but the "silent_mouth"
    mouth_images.append(silent_mouth)

    poppers = [load_and_scale(f"{image_path}/Poppers/{guy}", scalar) for guy in guys]
    for i, speaker in enumerate(speakers):
        popper = poppers[random.randint(0,1)] # Choose a random guy
        speakers[speaker].set_image(popper) # Set the image
        x = BLOCK_SIZE[0] * (i % cols) # x on the grid of guys
        y = BLOCK_SIZE[1] * (rows - (i // cols)) # y on the grid of guys
        speakers[speaker].set_position(x, y) # Set the position



    # The main loop
    pygame.mixer.init()
    pygame.mixer.music.load(f"Source/{audio_filename}")
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
            
            speaker.mouth = -1 # Silent
            for i in range(len(speaker.script)):

                # If between start and end for speakers[id] that speaker is talking
                if time_current in speaker.script[i][0]:
                    # Interpolate which phoneme is being said based on time passed
                    difference = speaker.script[i][0][-1] - speaker.script[i][0][0] + 1
                    threshold_gap = difference // len(speaker.script[i][1])

                    for p in range(len(speaker.script[i][1])):
                        threshold = speaker.script[i][0][0] + (p + 1) * threshold_gap
                        if(time_current < threshold):
                            speaker.mouth = speaker.script[i][1][p]
                            break
                    break

            # NOTE, UPDATE WILL HAPPEN LATER WHERE THE CORRECT MOUTH IS USED (TRANSPARENT SPRITESHEET UNAVAILABLE)
            screen.blit(speaker.image, speaker.pos) #draws the person
                #screen.blit(talking_mouth, speaker.pos)
            screen.blit(mouth_images[speaker.mouth], speaker.pos)

        pygame.display.flip() # Draw to screen
        dt = clock.tick(FPS) # How many milliseconds have passed
        time_current += dt

        # End condition
        if(not pygame.mixer.music.get_busy()):
            running = False
    pygame.mixer.music.stop()
    pygame.display.quit()
    pygame.quit()

    return "Success :D"