import pygame
import time
import random
# Tip: every coordinate in this program point to upper left corner of an object

pygame.init()


# width and  height for game window
width = 800
height = 600

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

# main window of game
gameDisplay = pygame.display.set_mode((width, height))

# Heading of main window
pygame.display.set_caption('Race Car')

# clock of the game
clock = pygame.time.Clock()

# image of the car
carImg = pygame.image.load("Images/Angry_Car.png")

# width and height of car image
car_width = 48
car_hight = 48

# sounds
crash_sound = pygame.mixer.Sound("Music/Car-Crash-Sound.ogg")
pygame.mixer.music.load("Music/Fire-Funk-Sound.ogg")

# action recieves name of another function
def button(msg, x, y, w, h, inactive_color, active_color, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
            # if action == "play":
            #     game_loop()
            # elif action == "quit":
            #     pygame.quit()
            #     quit()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x+(w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_font = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Let's Play Game", text_font)
        TextRect.center = ((width/2), (height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Play!!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()


def stuff_score_count(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("score : "+str(count), True, red)
    gameDisplay.blit(text, (0, 0))


# create objects 
def stuff(stuffx, stuffy, stuffw, stuffh, color):
    pygame.draw.rect(gameDisplay, color, [stuffx, stuffy, stuffw, stuffh])

# show the car
def car(x, y):
    gameDisplay.blit(carImg, (x, y))

#
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    text_font = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects(text, text_font)
    TextRect.center = ((width/2), (height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    text_font = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects("You Crashed", text_font)
    TextRect.center = ((width/2), (height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Try agian", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()


def game_loop():
    #-1 means play forever
    pygame.mixer.music.play(-1)

    x = (width * 0.45)
    y = (height * 0.8)

    x_change = 0

    stuff_startx = random.randrange(0, width)
    stuff_starty = -700
    stuff_speed = 7
    stuff_width = 100
    stuff_height = 100

    score_count = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # stuffx,stuffy,stuffw,stuffh,color
        stuff(stuff_startx, stuff_starty, stuff_width, stuff_height, red)
        stuff_starty += stuff_speed

        stuff_score_count(score_count)

        car(x, y)

        if x > width - car_width or x < 0:
            crash()

        if stuff_starty > height:
            stuff_starty = 0 - stuff_height
            stuff_startx = random.randrange(0, width)
            score_count += 1
            stuff_speed += 1

            # if (score_count % 5 == 0):

        if y < stuff_starty + stuff_height:
            if x > stuff_startx and x < stuff_startx + stuff_width or x + car_width > stuff_startx and x + car_width < stuff_startx + stuff_width:
                crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
