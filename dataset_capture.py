# Import OpenCV2 for image processing
import cv2
import os

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def dataset_capture_fun(id,course_id):
# Start capturing video 
    vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize sample face image
    count = 0

    assure_path_exists('dataSet/' +str(course_id)+'/'+str(id)+'/')

# Start looping
    while(True):

    # Capture video frame
        _, image_frame = vid_cam.read()

    # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
        for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (0,255,0), 3)
        
        # Increment sample face image
            count += 1
        # Save the captured image into the datasets folder
        #path= f'../dataSet\\{sem}\\{subject}\\{face_id}'
            path='dataSet/' +str(course_id)+'/'+str(id)+'/'
            cv2.imwrite( path + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', image_frame)
    # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

   # If image taken reach 100, stop taking video
        elif count>=40:
            print("Successfully Captured")
            break

# Stop video
    vid_cam.release()

# Close all started windows
    cv2.destroyAllWindows()
