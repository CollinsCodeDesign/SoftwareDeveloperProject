
import json
import pygame
import cv2
from gtts import gTTS
import os
from subprocess import Popen, PIPE
from pygame.locals import *
pygame.init()
        
def make_audio_message(message):
    # Language in which you want to convert 
    language = 'en'
    myobj = gTTS(text=message, lang=language, slow=False)
    myobj.save("welcome.mp3")   

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
        
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    
def checkClicked():
    click = pygame.mouse.get_pressed()
    x, y = 0,1
    click = 0
    if pygame.mouse.get_pos()[x] > x and pygame.mouse.get_pos()[x] < x + 100:
        if pygame.mouse.get_pos()[y] > y and pygame.mouse.get_pos()[y] < y + 50:
            return True
        else:
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
        
    start = True
    count_max = 0
    count_d = 10
    capture = cv2.VideoCapture(camera_input)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    screen = pygame.display.set_mode((frame_width ,frame_height + 100))
    pygame.display.set_caption(pygame_window_name)
    face_cascade = cv2.CascadeClassifier(face_xml_cascade)
    eye_cascade = cv2.CascadeClassifier(eye_xml_cascade)
    smile_cascade = cv2.CascadeClassifier(smile_xml_cascade)

    num = 0
    num2 = 0
    wait = True
    eye_detected = False
    # while wait:
    #     pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,640,480))
    #     button("GO!",550,480,100,50,(0,100,0),(0,255,0))
    #     pygame.display.update()
    #Continuely get camera frames
    while start:
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
        button("GO!",550,480,100,50,(0,100,0),(0,255,0))
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
        if checkClicked() == True:
            start = False
            pygame.display.quit()
            pygame.quit()
   
            
