
import json
import pygame
import cv2
from gtts import gTTS
import os
import pygame as pg
import time
from subprocess import Popen, PIPE
from pygame.locals import *
pygame.init()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
        
#----------------------------------------------------------------------

def make_audio_message(message):
    # Language in which you want to convert 
    language = 'en'
    myobj = gTTS(text=message, lang=language, slow=False)
    myobj.save("welcome.mp3")   

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

#----------------------------------------------------------------------
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True      
        return False
    
#-----------------------------------------------------------------------
class LoadJson:
    def __init__(self, jsonFile):
        with open(jsonFile,'r') as json_config:
            self.config = json.load(json_config)
            self.camera_input = int(self.config["camera_input"])
            self.face_xml_cascade = self.config["face_xml_cascade"]
            self.eye_xml_cascade = self.config["eye_xml_cascade"]
            self.smile_xml_cascade = self.config["smile_xml_cascade"]
            self.face_box_color = (int(self.config["face_box_color"].split(",")[0]),int(self.config["face_box_color"].split(",")[1]),int(self.config["face_box_color"].split(",")[2]))
            self.eye_box_color = (int(self.config["eye_box_color"].split(",")[0]),int(self.config["eye_box_color"].split(",")[1]),int(self.config["eye_box_color"].split(",")[2]))
            self.smile_box_color = (int(self.config["smile_box_color"].split(",")[0]),int(self.config["smile_box_color"].split(",")[1]),int(self.config["smile_box_color"].split(",")[2]))
            self.font_size_of_label = int(self.config["font_size_of_label"])
            self.color_of_face_label = (int(self.config["color_of_face_label"].split(",")[0]),int(self.config["color_of_face_label"].split(",")[1]),int(self.config["color_of_face_label"].split(",")[2]))
            self.color_of_eye_label = (int(self.config["color_of_eye_label"].split(",")[0]),int(self.config["color_of_eye_label"].split(",")[1]),int(self.config["color_of_eye_label"].split(",")[2]))
            self.color_of_smile_label = (int(self.config["color_of_smile_label"].split(",")[0]),int(self.config["color_of_smile_label"].split(",")[1]),int(self.config["color_of_smile_label"].split(",")[2]))
            self.line_thickness_of_boxes = int(self.config["line_thickness_of_boxes"])
            self.font_thickness_of_label = int(self.config["font_thickness_of_label"])
            self.adjust_label_x = int(self.config["adjust_label_x"])
            self.adjust_label_y = int(self.config["adjust_label_y"])
            self.pygame_window_name = self.config["pygame_window_name"]
            self.screen_added_width = int(self.config["screen_added_width"])
            self.screen_added_height = int(self.config["screen_added_height"])
            
#----------------------------------------------------------------------

if __name__ == "__main__":    
    settings = LoadJson('face_detector_config.json')   
    start = False
    #count_max = 0
    #count_d = 10
    capture = cv2.VideoCapture(settings.camera_input)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    screen = pygame.display.set_mode((frame_width + settings.screen_added_width,frame_height + settings.screen_added_height))
    pygame.display.set_caption(settings.pygame_window_name)
    face_cascade = cv2.CascadeClassifier(settings.face_xml_cascade)
    eye_cascade = cv2.CascadeClassifier(settings.eye_xml_cascade)
    smile_cascade = cv2.CascadeClassifier(settings.smile_xml_cascade)

    num = 0
    num2 = 0
    wait = True
    eye_detected = False
    def redrawWindow():
        greenButton.draw(screen,(0,0,0))
        
    greenButton = button((192, 192, 192),470,500,100,40, 'Start')
    while wait:
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(50,0,640,480))
        redrawWindow()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                wait = False
                start = True
                greenButton = button((192, 192, 192),470,500,100,40, 'Quit')
                time.sleep(1)
        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (20,100,100)
            else:
                greenButton.color = (192, 192, 192)
        if event.type == pygame.QUIT:
                start = False
                pygame.display.quit()
                pygame.quit()
                time.sleep(1)

#Continuely get camera frames
    while start:
        input_box1 = InputBox(250, 490, 100, 32)
        input_box2 = InputBox(250, 530, 100, 32)
        input_boxes = [input_box1, input_box2]

        redrawWindow()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
                box.update()
                box.draw(screen)
                
        pygame.display.update()        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                pygame.display.quit()
                pygame.quit()
                capture.release()
                time.sleep(2)
                
        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (20,100,100)
            else:
                greenButton.color = (192, 192, 192)
        ret, img = capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),settings.face_box_color,settings.line_thickness_of_boxes)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            font = cv2.FONT_HERSHEY_PLAIN 
            img = cv2.putText(img, 'Face', (x+settings.adjust_label_x,y+settings.adjust_label_y), font, settings.font_size_of_label, (settings.color_of_face_label), settings.font_thickness_of_label, cv2.LINE_AA)
            smile = smile_cascade.detectMultiScale(roi_color, 1.1, 40)
            for (sx,sy,sw,sh) in smile:
                cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),settings.smile_box_color,settings.line_thickness_of_boxes)
                img = cv2.putText(img, 'Smile',(x+sx+settings.adjust_label_x,y+sy+settings.adjust_label_y), font, settings.font_size_of_label, (settings.color_of_smile_label), settings.font_thickness_of_label, cv2.LINE_AA)
                
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if(len(eyes) > 0):
                eye_detected = True
            else:
                eye_detected = False
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),settings.eye_box_color,settings.line_thickness_of_boxes)
                img = cv2.putText(img, 'Eye',(x+ex+settings.adjust_label_x,y+ey+settings.adjust_label_y), font, settings.font_size_of_label, (settings.color_of_eye_label), settings.font_thickness_of_label, cv2.LINE_AA)
        # Window name in which image is displayed
        num = len(faces)
        cv2.imwrite('1.png',img)
        #out.write(img)
        faceImg = pygame.image.load('1.png')
        screen.blit(faceImg,(50,0))
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,480,200,580))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                capture.release()
                pygame.display.quit()
                pygame.quit()

        if(num != num2):
            print(' Faces ' + str(len(faces)) + '\n', end='', flush=True)
            num2 = num
        if (num >= 1 and pygame.display.get_active()):
            faceIcon = pygame.image.load('face.png')
            screen.blit(faceIcon,(0,480))
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,480,100,580),1)
            pygame.display.update()
# Audio mp3 played when face is detected            
#         if(count_max < num):
#             #os.system("mpg321 welcome.mp3")
#             #process = Popen(['mpg321', 'welcome.mp3'], stdout=PIPE, stderr=PIPE)
#             count_max = num
#         elif(0 == int(len(faces))):
#             count_d -= 1
#             if (count_d == 0):
#                 count_max = 0
#                 count_d = 10
                
        if (eye_detected and num >= 1):
            eyeIcon = pygame.image.load('eye.png')
            if pygame.display.get_active():
                screen.blit(eyeIcon,(100,480))
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,480,200,580),1)
                pygame.display.update()

   
            

