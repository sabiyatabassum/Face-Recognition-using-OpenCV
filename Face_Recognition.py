import cv2
import numpy as np
import os
#print('hello opencv')
#print('hai')

# face detection
def faceDetection(test_img):
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('Resources/haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=3)
    return faces, gray_img

#Labels for Training data

def labels_for_training_data(directory):
    faces =[]
    faceID=[]

    for path, subdirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                print("Skipping System file")
                continue
            id = os.path.basename(path)
            img_path=os.path.join(path, filename)
            print("Image Path", img_path)
            print("Id", id)
            test_img = cv2.imread(img_path)
            if test_img is None:
                print("Not loaded Properly")
                continue

            faces_rect, gray_img = faceDetection(test_img)
            if len(faces_rect) != 1:
                continue
            (x, y, w, h) = faces_rect[0]
            roi_gray=gray_img[y:y+w,x:x+h]
            faces.append(roi_gray)
            faceID.append(int(id))
    return faces, faceID

#Training classifier is called

def train_classifier(faces,faceID):
    face_recognizer= cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer

def draw_rect(test_img,face):
    (x,y,w,h)=face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

def put_text(test_img, label_name,x,y):
    cv2.putText(test_img,label_name,(x,y),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),3)



