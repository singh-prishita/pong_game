import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import time
from playsound import playsound

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all resources
imgBackground = cv2.imread("Resources/Backgrounds.png")
# imgBackgrounds = cv2.imread("Resources/Backgrounds.png")
print(imgBackground.shape)
imgGameOver = cv2.imread("Resources/Over.png")
imgBall = cv2.imread("Resources/strike.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/a.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/a.png", cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

num_frames = 0
start_time = time.time()

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 445)
            

            # h2, w2, _ = imgBat2.shape
            # y2 = y - h2//2
            # y2 = np.clip(y2, 20, 445)
            # x2 = x - w2//2


            if hand['type'] == "Left":
                x1 = x - w1//2
                img = cvzone.overlayPNG(img, imgBat1, (x1, y1))
                lmListLeft = hand["lmList"]
                fingersLeft = detector.fingersUp(hand)
                fingersLeft = sum(fingersLeft)
                # print(fingersLeft, speedX)
                if x1 < ballPos[0] < x1 + 10 + w1 and y1 < ballPos[1] < y1 + h1: 
                    playsound("Resources/air-hockey-puck-hitsb.mp3")   
                    speedX = -speedX # Change OX direction 
                    ballPos[0] += 30
                    score[0] += 1

                    if fingersLeft == 2 and speedX <0:
                        speedX = speedX +10
                
                    if fingersLeft == 2 and speedX >0:
                        speedX = speedX -10

                    if fingersLeft == 3 and speedX <0:
                        speedX = speedX 

                    if fingersLeft == 3 and speedX >0:
                        speedX = speedX 

                    if fingersLeft == 4 and speedX <0:
                        speedX = speedX -25

                    if fingersLeft == 4 and speedX >0:
                        speedX = speedX + 25  

            if hand['type'] == "Right":
                x2 = x - w1//2
                img = cvzone.overlayPNG(img, imgBat2, (x2, y1))
                lmListRight = hand["lmList"]
                if x2 - 40 < ballPos[0] < x2 + w1 and y1 < ballPos[1] < y1 + h1:
                    playsound("Resources/air-hockey-puck-hitsb.mp3")   
                    speedX = -speedX # Change OX direction
                    ballPos[0] -= 30
                    score[1] += 1

    # Game Over
    if ballPos[0] < 40  or ballPos[0] > 1200:
        gameOver = True
    
    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[1] + score[1]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)

    # If game not over move the ball
    else:

        # Move the ball
            # Change OY direction
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        # Display score on the image
            # Left player (hand)
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            # Rigth player (hand)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    # Cam show
    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120)) 

       # Increment frame count
    num_frames += 1

    # Calculate elapsed time and FPS
    end_time = time.time()
    elapsed_time = end_time - start_time
    fps = num_frames / elapsed_time

    # Display the FPS on the frame
    cv2.putText(img, f"FPS: {round(fps, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Prishita", img)
    key = cv2.waitKey(1)

    # Reload the game by pressing "r"
    if key == ord("r"):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/Over.png")