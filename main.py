import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
light_green = (144, 238, 144)

# we use find these colour codes
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

pygame.display.update()

clock = pygame.time.Clock()  # to define fps

img = pygame.image.load('C:/Users/srinj/PycharmProjects/Snakegame/snakehead.png')  # snake head
pause_img = pygame.image.load('C:/Users/srinj/Downloads/pause.jpg')
over = pygame.image.load('C:/Users/srinj/Downloads/gameover.jpg')
start_screen = pygame.image.load('C:/Users/srinj/Downloads/starting.jpg')
background = pygame.image.load('background.png')
apple_img = pygame.image.load('C:/Users/srinj/PycharmProjects/Snakegame/Apple.PNG')
direction = 'right'  # defines direction of snake
AppleThickness = 25

FPS = 20

small_font = pygame.font.SysFont('comicsansms', 25)  # its a font object(    , font size)
medium_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 80)


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        gameDisplay.blit(pause_img, (0, 0))
        message_to_screen('PAUSED', black, -100, size=large_font)
        message_to_screen('Press C to continue or Q to quit', black, 25)
        pygame.display.update()
        clock.tick(5)


def score(score):
    text = small_font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0, 0])


def snake(block_size, snakeList):

    if direction == 'right':  #to rotate snake head
         head = pygame.transform.rotate(img, 0)
    if direction == 'up':
        head = pygame.transform.rotate(img, 90)
    if direction == 'left':
        head = pygame.transform.rotate(img, 180)
    if direction == 'down':
        head = pygame.transform.rotate(img, 270)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, (21, 213, 66), [XnY[0], XnY[1], block_size, block_size])  # draws a rectangle. the list is [x , y , width, height]


def text_objects(text, colour, size=small_font):
    textSurface = size.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, colour, y_displace=0, size=small_font):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def game_intro():  #Main menu
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        gameDisplay.blit(start_screen, (0, 0))

        message_to_screen('Welcome to Slither', green, -100, size=large_font)
        message_to_screen('The objective of the game is to eat apples', black, -30)
        message_to_screen('Good Luck', black, 10)
        message_to_screen('Press C to play and Q to quit', red, 180)
        pygame.display.update()
        clock.tick(15)


def apple_generaton():  #position of apple
    apple_x = round(random.randrange(0, display_width - AppleThickness))  # so that part of block do not spawn outside. rounding is done to align apple with snake
    apple_y = round(random.randrange(0, display_height - AppleThickness))
    return apple_x, apple_y


def gameLoop():  # the game loop
    global direction
    direction = 'right'
    gameExit = False
    gameOver = False  # for game over screen

    lead_x = display_width // 2
    lead_y = display_height // 2
    block_size = 20  # defines change in position of object

    lead_x_change = 10
    lead_y_change = 0  # defines change in position of object

    snakeList = []
    snakeLength = 1

    apple_x, apple_y = apple_generaton()

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            gameDisplay.blit(over, (0, 0))
            message_to_screen("Game Over ", red, -50, large_font)
            message_to_screen('Press C to play gain or Q to quit', black, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit event
                gameExit = True

            if event.type == pygame.KEYDOWN:  # if key is pressed
                if event.key == pygame.K_LEFT:  # left arrow key
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0  # so that object keeps moving while ikey is pressed and does not move diagonally
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_ESCAPE:
                    pause()

        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:  # to set boundary. keep the value equal to height or width of the window
            gameOver = True

        lead_x += lead_x_change  # so that object keeps moving while ikey is pressed
        lead_y += lead_y_change

        gameDisplay.fill(white)  # fills the display with white
        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(apple_img, (apple_x, apple_y))  #It creates the apple

        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:  # to control length of the length of snake
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        pygame.display.update()

        if apple_x < lead_x < apple_x + AppleThickness or apple_x + AppleThickness > lead_x + block_size > apple_x:
            if apple_y < lead_y < apple_y + AppleThickness or apple_y + AppleThickness > lead_y + block_size > apple_y:
                apple_x, apple_y = apple_generaton()
                snakeLength += 1  # to lengthen the snake

        score(snakeLength-1)

        pygame.display.update()

        clock.tick(FPS)


game_intro()
gameLoop()
