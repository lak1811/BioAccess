import cv2
import face_recognition
import os



def show_camera(known_faces,known_faces_folder,picam2):
    
    # Grab images as numpy arrays and leave everything else to OpenCV.
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    cv2.startWindowThread()
    
    
    #starting the camera and making it loop until it finds a face
    picam2.start() 
    stop_camera=False
    try:

        while not stop_camera:
            #taking in the frames from my picamera and updating them with this loop
            im = picam2.capture_array()

            #make these frames to a specific color which helps the model 
            rgb_im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            #the variable faces is detection of faces. the minNeighbor and scalefactor are default, but 
            #good to include
            faces = face_detector.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
            #iterate over the found faces using x,y,width and height
            for (x, y, w, h) in faces:
                #try to find faces in the current frame
                face_image = face_recognition.face_locations(rgb_im[y:y+h,x:x+w],model='hog')
                face_encoding = face_recognition.face_encodings(rgb_im,face_image)



                # if a random face is found, it will compare it to all the faces in my dataset
                if face_encoding:
                    matches = face_recognition.compare_faces(known_faces, face_encoding[0])
                    name = "Unknown"
                    #if the picture is found in my datasaet, then the loop stops and returns ID
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = os.listdir(known_faces_folder)[first_match_index].split(".")[0]
                        name = name.split('_')[0]

                        stop_camera=True
                        
                        


            cv2.imshow("Running Webcam", im)
            if stop_camera:
                #stopping camera and returning value
                cv2.destroyAllWindows()
                picam2.stop()
                print (f"The ID found is {name}")
                return name
    except Exception as e:
        print(f"error in show_camera {e}")
            
            
    
            
        
    



if __name__ == "__main__":
    # This block will only run if the script is executed directly, not when it's imported
    show_camera()

    for file_name in os.listdir(known_faces_folder):
        image_path = os.path.join(known_faces_folder, file_name)
        known_face_image = face_recognition.load_image_file(image_path)
        known_face_encoding = face_recognition.face_encodings(known_face_image)[0]
        known_faces.append(known_face_encoding) """
