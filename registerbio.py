import os
import cv2
import time
from picamera2 import Preview
def register(data,picam2):
    
    #foldername
    output_folder='dataset'
    #start camera
   
   
    picam2.start_preview(Preview.QTGL)
    counter=10
    picam2.start()
    #make a counter
    for timer in range(0,10,1):
        counter-=1
        print (f"{counter} seconds left until start")
        time.sleep(1)

    counter1=0
    #take 10 pictures of the user
    print ("START")
    for x in range(0,10,1):
        counter1+=1
        name=f"{data}_{counter1}.jpg"
        image_path = os.path.join(output_folder, name)
        time.sleep(1)
        
        picam2.capture_file(image_path)
        print (f"Picture nr {counter1} has been taken")
    picam2.stop()
    picam2.stop_preview()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    # This block will only run if the script is executed directly, not when it's imported
    register()