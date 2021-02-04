import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

#Continuely get camera frames
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    

   



    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        # font 
        font = cv2.FONT_HERSHEY_PLAIN
        # org 
        org = (x,y-5) 
        # fontScale 
        fontScale = 1   
        # Black color in BGR 
        color = (110, 110, 110)   
        # Line thickness of 2 px 
        thickness = 2   
        # Using cv2.putText() method
        img = cv2.putText(img, 'Face', (x-1,y-6), font,  
                           fontScale, (255,255,255), thickness, cv2.LINE_AA)
        img = cv2.putText(img, 'Face', org, font,  
                           fontScale, color, thickness, cv2.LINE_AA)
        smile = smile_cascade.detectMultiScale(roi_color, 1.1, 40)
        for (sx,sy,sw,sh) in smile:
            cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(255,150,0),2)
            img = cv2.putText(img, 'Smile',(x+sx,y+sy), font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
            
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            img = cv2.putText(img, 'Eye',(x+ex,y+ey), font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
    # Window name in which image is displayed 
    window_name = 'Face eye smile detector' 
    cv2.imshow(window_name,img)
    if ret == True:
        # Write the frame into the file 'output.avi'
        out.write(img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()