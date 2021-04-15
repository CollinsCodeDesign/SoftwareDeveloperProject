
import json
import cv2
import os
import time

    
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

def main():
    settings = LoadJson('face_detector_config.json')   
    start = False
    wait = True
    config = False
    eye_detected = False
    num = 0
    num2 = 0
    
    #count_max = 0
    #count_d = 10
    
    capture = cv2.VideoCapture(settings.camera_input)
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    
    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    
    face_cascade = cv2.CascadeClassifier(settings.face_xml_cascade)
    eye_cascade = cv2.CascadeClassifier(settings.eye_xml_cascade)
    smile_cascade = cv2.CascadeClassifier(settings.smile_xml_cascade)

# #Continuely get camera frames
    while True:
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
        #time.sleep(2)
        #out.write(img)
        if(num != num2):
            print(' Faces ' + str(len(faces)) + '\n', end='', flush=True)
            num2 = num

if __name__ == "__main__":    
    main()

   
            

