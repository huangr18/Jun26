import cv2
import numpy as np
import time
import PoseModule as pm

# run on camera
#cap = cv2.VideoCapture(0)
#vedio demo
def runcv(filename):
    cap = cv2.VideoCapture(("static/files/%s"%filename))
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    color = (225, 0 ,225)
    bar = 0
    per = 0
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    while True:
        success, img = cap.read()
        #success, src = cap.read()
        #img = cv2.flip(src, 180)
        img = cv2.resize(img, size)
        #img = cv2.resize(img, (1179, 2556))
        # img = cv2.imread("PoseImage/jumping_Jacks.jpg")
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            # Right Arm
            upAngle = detector.findAngle(img, 16, 0, 15, False)
            lowAngle = detector.findAngle(img, 28, 24, 27)

            upper = np.interp(upAngle,(30, 300), (100, 0))
            lowper = np.interp(lowAngle,(340, 350), (100, 0)) 

            per = (upper + lowper) / 2 
            print(lowAngle, lowper)
            #print(raper)

            upbar = np.interp(upAngle,(30, 300), (70, 630))
            lowbar = np.interp(lowAngle,(340, 350), (70, 630))

            bar = (upbar + lowbar) / 2
            #print(bar)

            # check jumping jacks
            color = (255, 0 ,255)
            if upper and lowper == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if upper and lowper == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            if count >= 100 and count < 106:
                cv2.putText(img, "stop", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 0), 4)

        #print(count)

        # Bar x+75
        cv2.rectangle(img, (1100, 70), (1200, 630), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1200, 630), color, cv2.FILLED)
        #print(bar)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        #cv2.rectangle(img, (0,450), (250, 720), (0, 255, 0), cv2.FILLED)
        #cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)



        cv2.imshow("Image", img)
        cv2.waitKey(1)