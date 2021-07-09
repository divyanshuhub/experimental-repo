from flask import Flask, render_template, Response
#import final_run
#import gui_final
import cv2
from cv2 import VideoCapture, resize, cvtColor, rectangle, putText, imshow, waitKey, COLOR_BGR2RGB, FONT_HERSHEY_SIMPLEX
from final_fns import face_locations, face_encodings, compare_faces, face_distance, markAttendance
import os
from pandas import read_csv
from numpy import argmin


app = Flask(__name__)

#@app.route('/')
#def dynamic_page():
 #   #return final_run.funs()
  #  return gui_final.funs()

path = "img"
classNames = []
nameList = os.listdir(path)
for img in nameList:
    classNames.append(os.path.splitext(img)[0])

# List of encodings od known faces
df = read_csv("Encodings_db.csv")
df.drop(df.columns[[0]], axis = 1, inplace = True)
encodedListKnown = df.values.tolist()

cap = cv2.VideoCapture(0)

#rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#for local webcam use
# cv2.VideoCapture(0)

def gen_frames():
    while True:  # video is a just a large no. of images
        success, img = cap.read()
        # reducing the size of image bcz its real time

        imgSmall = resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cvtColor(imgSmall, COLOR_BGR2RGB)

        # finding the encoding of the image from the webcam:-

        # there might be multiple faces so we removed the [0] after it as then it would have only taken the first location
        camFaceLocs = face_locations(imgSmall)
        # similarly here we are giving camFaceLocs, the face location as argument for encodings
        camFaceEncodings = face_encodings(imgSmall, camFaceLocs)

        # finding the matches
        # first we will iterate through all the faces found in the cam
        for encodeFace, faceLoc in zip(camFaceEncodings, camFaceLocs):
            matches = compare_faces(encodedListKnown, encodeFace)
            faceDist = face_distance(encodedListKnown, encodeFace)
            # it will give us the values for all the faces from the list, lowest distance will be the best match
            # print(faceDist)
            matchIndex = argmin(faceDist)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                # to show box in webcam with name
                y1, x2, y2, x1 = faceLoc
                # multiplying the location coordinates by 4 bcz be derived them for scaled down image
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # addition box for name space
                rectangle(img, (x1, y1 - 35), (x2, y2), (0, 255, 0))
                # name as text
                putText(img, name, (x1 + 6, y2 - 6), FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # calling the func
                markAttendance(name)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='8000', debug=True)
    app.run(debug=True)
