import face_recognition
import cv2
import os
from tkinter import messagebox
def validify():


    def check(x):
        #read images from path given in parameter x
        image=cv2.imread(x)
        
        faces = face_recognition.face_locations(image)
        if not faces:
            # If a face is detected, proceed with encoding
            
            try:
                os.remove(x)
                print (f"File {x} is now deleted")
                history.append(x)
            except OSError as e:
                print (f"Error deleting file {x}, because of {e}")
            

    history=[]
    counter=0
    dataset_folder="/home/lak1811/project/env/dataset"
    for image_file in os.listdir(dataset_folder):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(dataset_folder, image_file)
            check(image_path)
            counter+=1
            print (f"Picture number {counter} is being checked")
    cv2.destroyAllWindows()
    print ("-----------------------------------------------")
    print("IMAGES THAT HAS BEEN DELETED:")
    if history:
        finalstr=""

        for temp in range(0,len(history),1):
            finalstr+=history[temp]
            finalstr+="\n"
        messagebox.showinfo(f"{len(history)} Deleted files", f"Files that were not accepted \n {finalstr}")
    else:
        print ('No images')
    
if __name__ == "__main__":
    # This block will only run if the script is executed directly, not when it's imported
    validify()
    
