
import json
import pygame
import cv2
from gtts import gTTS
import os
import pygame as pg
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

def make_audio_message(message):
    # Language in which you want to convert 
    language = 'en'
    myobj = gTTS(text=message, lang=language, slow=False)
    myobj.save("welcome.mp3")   

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


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
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True      
        return False



if __name__ == "__main__":
    with open('face_detector_config.json','r') as json_config:
        config = json.load(json_config)
        camera_input = int(config["camera_input"])
        face_xml_cascade = config["face_xml_cascade"]
        eye_xml_cascade = config["eye_xml_cascade"]
        smile_xml_cascade = config["smile_xml_cascade"]
        face_box_color = (int(config["face_box_color"].split(",")[0]),int(config["face_box_color"].split(",")[1]),int(config["face_box_color"].split(",")[2]))
        eye_box_color = (int(config["eye_box_color"].split(",")[0]),int(config["eye_box_color"].split(",")[1]),int(config["eye_box_color"].split(",")[2]))
        smile_box_color = (int(config["smile_box_color"].split(",")[0]),int(config["smile_box_color"].split(",")[1]),int(config["smile_box_color"].split(",")[2]))
        font_size_of_label = int(config["font_size_of_label"])
        color_of_face_label = (int(config["color_of_face_label"].split(",")[0]),int(config["color_of_face_label"].split(",")[1]),int(config["color_of_face_label"].split(",")[2]))
        color_of_eye_label = (int(config["color_of_eye_label"].split(",")[0]),int(config["color_of_eye_label"].split(",")[1]),int(config["color_of_eye_label"].split(",")[2]))
        color_of_smile_label = (int(config["color_of_smile_label"].split(",")[0]),int(config["color_of_smile_label"].split(",")[1]),int(config["color_of_smile_label"].split(",")[2]))
        line_thickness_of_boxes = int(config["line_thickness_of_boxes"])
        font_thickness_of_label = int(config["font_thickness_of_label"])
        adjust_label_x = int(config["adjust_label_x"])
        adjust_label_y = int(config["adjust_label_y"])
        pygame_window_name = config["pygame_window_name"]
        
    start = False
    count_max = 0
    count_d = 10
    capture = cv2.VideoCapture(camera_input)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    screen = pygame.display.set_mode((frame_width ,frame_height + 100))
    pygame.display.set_caption(pygame_window_name)
    face_cascade = cv2.CascadeClassifier(face_xml_cascade)
    eye_cascade = cv2.CascadeClassifier(eye_xml_cascade)
    smile_cascade = cv2.CascadeClassifier(smile_xml_cascade)

    num = 0
    num2 = 0
    wait = True
    eye_detected = False
    def redrawWindow():
        greenButton.draw(screen,(0,0,0))
    greenButton = button((192, 192, 192),470,500,150,50, 'Start')
    while wait:
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,640,480))
        redrawWindow()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                wait = False
                start = True
        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (20,100,100)
            else:
                greenButton.color = (192, 192, 192)
        if event.type == pygame.QUIT:
                start = False
                pygame.display.quit()
                pygame.quit()
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
                print('clicked')
        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (20,100,100)
            else:
                greenButton.color = (192, 192, 192)
        ret, img = capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),face_box_color,line_thickness_of_boxes)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            font = cv2.FONT_HERSHEY_PLAIN 
            img = cv2.putText(img, 'Face', (x+adjust_label_x,y+adjust_label_y), font, font_size_of_label, (color_of_face_label), font_thickness_of_label, cv2.LINE_AA)
            smile = smile_cascade.detectMultiScale(roi_color, 1.1, 40)
            for (sx,sy,sw,sh) in smile:
                cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),smile_box_color,line_thickness_of_boxes)
                img = cv2.putText(img, 'Smile',(x+sx+adjust_label_x,y+sy+adjust_label_y), font, font_size_of_label, (color_of_smile_label), font_thickness_of_label, cv2.LINE_AA)
                
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if(len(eyes) > 0):
                eye_detected = True
            else:
                eye_detected = False
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),eye_box_color,line_thickness_of_boxes)
                img = cv2.putText(img, 'Eye',(x+ex+adjust_label_x,y+ey+adjust_label_y), font, font_size_of_label, (color_of_eye_label), font_thickness_of_label, cv2.LINE_AA)
        # Window name in which image is displayed
        num = len(faces)
        cv2.imwrite('1.png',img)
        #out.write(img)
        faceImg = pygame.image.load('1.png')
        screen.blit(faceImg,(0,0))
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
            
        if(count_max < num):
            #os.system("mpg321 welcome.mp3")
            process = Popen(['mpg321', 'welcome.mp3'], stdout=PIPE, stderr=PIPE)
            count_max = num
        elif(0 == int(len(faces))):
            count_d -= 1
            if (count_d == 0):
                count_max = 0
                count_d = 10
                
        if (eye_detected and num >= 1):
            eyeIcon = pygame.image.load('eye.png')
            if pygame.display.get_active():
                screen.blit(eyeIcon,(100,480))
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,480,200,580),1)
                pygame.display.update()

   
            
