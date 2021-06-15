from cv2 import imread, cvtColor, COLOR_BGR2RGB
from final_fns import face_locations, face_encodings
from os import listdir
import pandas as pd

path = "img"
images = []
nameList = listdir(path)
print(nameList)

for img in nameList:
    curImg=imread(f'{path}/{img}')
    images.append(curImg)


#encoding

def findEncodings(images):
    encodedList = []
    for img in images:
        img = cvtColor(img, COLOR_BGR2RGB)
        #encode = face_recognition.face_encodings(img)[0]
        camFaceLocs = face_locations(img)
        # similarly here we are giving camFaceLocs, the face location as argument for encodings
        encode = face_encodings(img, camFaceLocs)[0]
        encodedList.append(encode)
    return encodedList

encodedListKnown = findEncodings(images)
print("ENcoding COMPLETE")

df = pd.DataFrame(encodedListKnown)
df.to_csv("Encodings_db.csv")
print("Encoding Database - 'Encodings_db' saved")