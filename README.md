# Automatic-Attendance-System
Automatic Attendance System Using Face recognition

The project is developed using python 3.8       
Web application :Flask Library in Python(Flask is Ligthweight web frame and suitable for small web applications)      
Database using : MySql
  		
1.app.py : Applicatons root file.  
      
2.Dataset Capture:    
    Library used: OpenCV  (Open Source Computer Vision)  
    Others: Haar cascade      
    Face detection using Haar cascades is a machine learning based approach where a cascade function is trained with a set of input data. There are classifiers for face, eyes,smile,etc.I have used frontal face.      
      
3.Training data and Recognition:      
    Library used: OpenCV and NumPy(Numpy is used to create large ,multidimentional arrays and matrices)  
    Others: LBPH recogniser   
    
    LBP(Local Binary Patterns):It labels the pixels of image by thresholding the neighbourhood of each pixel and gives the result as a binary number.for eg.For a pixel value greater than thresholding value it given as white(i.e. 1) O.W.black(i.e.0)          
    LBPH(Local Binary Patterns Histograms): The LBP is combined with histograms to represent the face images with a data vector.
  
 4.Make CSV :     
     Library used: csv    
     Creating csv file subjectwise with students name enrolled for that course And marking the attendance subjectwise .
     
 5.Remove:
     To remove data like the captured images of student who removed from the course and removing the data if course removed. 
