import cv2
import mediapipe as mp
from pyfirmata import Arduino, SERVO, util
from time import sleep

port = 'COM7'
pin = 9  # 360
pin2 = 10 # 360
pin3 = 11 # 360

board = Arduino(port)

board.digital[pin].mode = SERVO
board.digital[pin2].mode = SERVO
board.digital[pin3].mode = SERVO

cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def get_landmark_coords(pose_results):
    landmark_coords = {}
    if pose_results.pose_landmarks is not None:
        for i, landmark in enumerate(pose_results.pose_landmarks.landmark):
            landmark_coords[f"Landmark {i}"] = (landmark.x, landmark.y)
    return landmark_coords


prev_y16, prev_y12, prev_y11, prev_y15, prev_ybody = None, None, None, None, None


def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.095)


def check_and_rotate_hand(coord, prev_coord, pin):
    global board


    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.01:
            print(f"Hand {pin} NONE movement")
            rotateservo(pin, 90)

        elif coord is not None and coord > prev_coord:
            print(f"Hand {pin} is moving upwards")
            rotateservo(pin, 180)

        elif coord is not None and coord < prev_coord:
            print(f"Hand {pin} is moving downwards")
            rotateservo(pin, 0)


    else:
        print("nishto")


ybody = None

def check_and_rotate_body(coord, prev_coord):
    global pin, pin2, pin3

    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.01:
            print('Body NONE movement')
            rotateservo(pin3, 90)

        elif coord is not None and prev_coord is not None and coord > prev_coord:
            print('Body is moving upwards')
            rotateservo(pin, 180)
            rotateservo(pin2, 180)
            rotateservo(pin3, 180)

        elif coord is not None and prev_coord is not None and coord < prev_coord:
            print('Body is moving downwards')
            rotateservo(pin, 0)
            rotateservo(pin2, 0)
            rotateservo(pin3, 0)


rotateservo(pin, 90)
rotateservo(pin2, 90)
rotateservo(pin3, 90)



while True:

    # read frame
    ret, frame = cap.read()

    # frame = cv2.resize(frame, (1000, 1000))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(frame_rgb)

    mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    landmark_coords = get_landmark_coords(pose_results)

    y16 = landmark_coords['Landmark 16'][1] if 'Landmark 16' in landmark_coords else None
    y15 = landmark_coords['Landmark 15'][1] if 'Landmark 15' in landmark_coords else None
    y12 = landmark_coords['Landmark 12'][1] if 'Landmark 12' in landmark_coords else None
    y11 = landmark_coords['Landmark 11'][1] if 'Landmark 11' in landmark_coords else None

    if y12 is not None and y11 is not None:
        ybody = (y12 + y11) / 2

        # print(y16)

    print("~~~~~~~~~~~~")

    check_and_rotate_hand(y16, prev_y16, pin)
    check_and_rotate_hand(y15, prev_y16, pin3)
    check_and_rotate_body(ybody, prev_ybody)

    print("~~~~~~~~~~~~")

    prev_y16, prev_y15, prev_y12, prev_y11, prev_ybody = y16, y15, y12, y11, ybody

    cv2.imshow('Output', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()