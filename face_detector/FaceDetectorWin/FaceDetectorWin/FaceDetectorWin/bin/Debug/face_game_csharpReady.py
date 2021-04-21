import pygame
import time
import random
import cv2

pygame.init()

#Needs a little more work and intigration with FaceBox collision detection
#For now use the arrow keys to move left and right
#I have created a button class so we can easily add more buttons

display_width = 640
display_height = 480

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0, 200, 0)

bright_red = (255,0,0)
bright_green = (0,255,0)

faceBox_width = 255

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

def saveDisplay(display):
    try:
        pygame.image.save(display,"screenshot.jpeg")
    except:
        print("An exception occurred")

def crash():
    message_display('Game Over!')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    saveDisplay(gameDisplay)
    time.sleep(1)
    
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
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Facebox Dodge Game", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Play!",100,400,150,100, green, bright_green, "play")
        button("Quit",400,400,150,100, red, bright_red, "quit")
        mouse = pygame.mouse.get_pos()
        
        #print(mouse)
        
        #pygame.draw.rect(gameDisplay, red, (1300,900,150,100))
        
        pygame.display.update()
        clock.tick(5)


def game_loop():
    x = (display_width * 0.44)
    y = (display_height * 0.75)
    thing_startx = random.randint(0, display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100
    
    dodged = 0

    gameExit = False
    capture = cv2.VideoCapture(0)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    #screen = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption("Facebox Dodge Game")
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    saveEO = True
    while not gameExit:
        ret, img = capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            font = cv2.FONT_HERSHEY_PLAIN 
            img = cv2.putText(img, 'Face', (x+5,y+15), font, 1, (0,255,0), 1, cv2.LINE_AA)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        cv2.imwrite('1.png',img)
        Backimg = pygame.image.load('1.png')
#         x += x_change
        gameDisplay.blit(Backimg, (0,0))
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        faceBox(x,y)
        things_dodged(dodged)
        
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randint(0,display_width)
            dodged += 1
            thing_speed += 0.15
            thing_width += (dodged * 1)
        
        if y < thing_starty+thing_height:
            right_corner= int(x) + faceBox_width
            #crash is detected if the object is between two points
            if  thing_startx >= int(x) - 85 and right_corner + 85 >= (thing_startx + thing_width):
                capture.release()
                crash()
        
        pygame.display.update()
        if saveEO:
            saveDisplay(gameDisplay)
            saveEO = False
        else:
            saveEO = True
        clock.tick(160)

#game_intro()
game_loop()
pygame.quit()
quit()

