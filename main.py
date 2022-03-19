import mediapipe as mp
import cv2
from math import sqrt
import win32api
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click = 0

video = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        imageHeight, imageWidth, _ = image.shape

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                          )

        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:

                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                           normalizedLandmark.y,
                                                                                           imageWidth, imageHeight)

                    point = str(point)

                    if point == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            indexfingertip_x = pixelCoordinatesLandmark[0]
                            indexfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((indexfingertip_x * 4, indexfingertip_y * 5))

                        except:
                            pass

                    elif point == 'HandLandmark.MIDDLE_FINGER_TIP':
                        try:
                            middlefingertip_x = pixelCoordinatesLandmark[0]
                            middlefingertip_y = pixelCoordinatesLandmark[1]

                        except:
                            pass

                    try:
                        Distance_x = sqrt(
                            (indexfingertip_x - middlefingertip_x) ** 2 + (indexfingertip_x - middlefingertip_x) ** 2)
                        Distance_y = sqrt(
                            (indexfingertip_y - middlefingertip_y) ** 2 + (indexfingertip_y - middlefingertip_y) ** 2)
                        if -10 < Distance_x and Distance_y < 10:
                            click += 1
                            if click % 5 == 0:
                                print("Left click working")
                                pyautogui.leftClick()
                    except:
                        pass

        cv2.imshow('Virtual Mouse', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
