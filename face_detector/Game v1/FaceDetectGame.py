import pygame
import time
import random

pygame.init()

#Needs a little more work and intigration with FaceBox collision detection
#For now use the arrow keys to move left and right
#I have created a button class so we can easily add more buttons

display_width = 1800
display_height = 1200

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0, 200, 0)

bright_red = (255,0,0)
bright_green = (0,255,0)

faceBox_width = 225

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Facebox Dodging')
clock = pygame.time.Clock()

faceBoxImg = pygame.image.load('square.png')

def things_dodged(count):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def faceBox(x,y):
    gameDisplay.blit(faceBoxImg,(x,y))

def crash():
    message_display('Game Over!')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',150)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
    time.sleep(2)
    
    game_loop()

    #(message, x value, y value, width, height, inactive color, active color)
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    
    click = pygame.mouse.get_pressed()
    print(click)
    
    #print(mouse)
        
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            #print("Pierce")
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
            
    smallText = pygame.font.Font("freesansbold.ttf", 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)
        
    
def game_intro():
    
    intro = True
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',150)
        TextSurf, TextRect = text_objects("Facebox Dodge Game", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Play!",400,900,150,100, green, bright_green, "play")
        button("Quit",1300,900,150,100, red, bright_red, "quit")
        mouse = pygame.mouse.get_pos()
        
        #print(mouse)
        
        #pygame.draw.rect(gameDisplay, red, (1300,900,150,100))
        
        pygame.display.update()
        clock.tick(5)


def game_loop():
    x = (display_width * 0.44)
    y = (display_height * 0.75)

    x_change = 0
    
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100
    
    dodged = 0

    gameExit = False

    while not gameExit:
        
        for event in pygame.event.get() :
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
        
        
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        faceBox(x,y)
        things_dodged(dodged)
        
        if x > display_width - faceBox_width or x < 0:
            crash()
        
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 0.15
            thing_width += (dodged * 1.0000005)
        
        if y < thing_starty+thing_height:
            print('y crossover')
            
            if x > thing_startx and x < thing_startx + thing_width or x + faceBox_width > thing_startx and x + faceBox_width < thing_startx + thing_width:
                print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(144)

game_intro()
game_loop()
pygame.quit()
quit()
