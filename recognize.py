import os
import csv
import cv2
from datetime import date


def detect(course_id):
    filename = str(course_id)+'.csv'

    fname = 'trainer/trainingData.yml'
    if not os.path.isfile(fname):
        print('first train the data')
        exit(0)


    names = {}
    labels = []
    students = []
    today=date.today()
    today_str=str(today)
    #print(today_str)

    def getdata():
        with open(filename,'r') as f:
            data = csv.reader(f)
            next(data)
            lines = list(data)
            for line in lines:
                names[int(line[0])] = line[1]


    
    def  markPresent(name):
        with open(filename,'r') as f:
            data = csv.reader(f)
            lines = list(data)
            print(lines)
            f.seek(0)
            lno=0
            n=-1    
            if(today_str not in lines[0]):
                for line in lines:
                    line.append(0)
                lines[0][-1]=today_str
            
            n=lines[0].index(today_str)
            for line in lines:
                if line[1]==name:
                    line[n]=1
                        
                
            with open(filename,'w') as g:
                writer = csv.writer(g,lineterminator='\n')
                writer.writerows(lines)
            
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)


    getdata()
    print('Total students :',names)

    recognizer = cv2.face.LBPHFaceRecognizer_create() #LOCAL BINARY PATTERNS HISTOGRAMS Face Recognizer

    recognizer.read(fname) # read the trained yml file

    num=0
    while True:   
        ret, img = cap.read()
        #img = cv2.rotate(img, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        #img = cv2.rotate(img, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray)
        final = cv2.medianBlur(equ, 3)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        justlabels={}

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            label,confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print('label:',label)
            print('confidence:',confidence)
            predicted_name = names[label]
            if confidence > 50 :
                confidence = 100 - round(confidence)
                cv2.putText(img, predicted_name +str(confidence) +'%', (x+2,y+h-4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),3)
                labels.append(label)
                students.append(names[label])
                totalstudents = set(students)
                justlabels = set(labels)
                print('student Recognised : ',totalstudents,justlabels)


                for i in justlabels:
                    if labels.count(i)>40:
                        markPresent(names[label])
                        
            cv2.imshow('Face Recognizer',img)
            k = cv2.waitKey(30) & 0xff == ord('q')
            num+=1
            if num > 50:
                break
            
        if num > 100 :
            cap.release()              
            cv2.destroyAllWindows()
            print('we are done!')
            break




