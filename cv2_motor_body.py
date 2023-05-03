import cv2
import mediapipe as mp
from pyfirmata import Arduino, SERVO, util
from time import sleep

port = 'COM5'
pin = 9 # 360
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
    for i, landmark in enumerate(pose_results.pose_landmarks.landmark):
        landmark_coords[f"Landmark {i}"] = (landmark.x, landmark.y)
    return landmark_coords


prev_y16, prev_y12, prev_y11, prev_y15, prev_ybody = None, None, None, None, None


def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)


def check_and_rotate_hand(coord, prev_coord, pin):
    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.05:
            print('something is NOT moving')
            rotateservo(pin, 90)

        elif coord is not None and prev_coord is not None and coord > prev_coord:
            print('something is moving up')
            rotateservo(pin, 80)  # nagore

        elif coord is not None and prev_coord is not None and coord < prev_coord:
            print('something is moving down')
            rotateservo(pin, 100)  # nadolu


def check_and_rotate_body(coord, prev_coord):
    global pin, pin2, pin3

    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.05:
            print('something is NOT moving')
            rotateservo(pin2, 90)

        elif coord is not None and prev_coord is not None and coord > prev_coord:
            print('something is moving up')
            rotateservo(pin, 80)  # nagore
            rotateservo(pin2, 80)  # nagore
            rotateservo(pin3, 80)  # nagore

        elif coord is not None and prev_coord is not None and coord < prev_coord:
            print('something is moving down')
            rotateservo(pin, 100)  # nadolu
            rotateservo(pin2, 100)  # nadolu
            rotateservo(pin3, 100)  # nadolu


rotateservo(pin, 90)
rotateservo(pin2, 90)
rotateservo(pin3, 90)

while True:

    rotateservo(pin, 90)
    rotateservo(pin2, 90)
    rotateservo(pin3, 90)

    # read frame
    ret, frame = cap.read()
    try:

        # frame = cv2.resize(frame, (350, 600))

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pose_results = pose.process(frame_rgb)

        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmark_coords = get_landmark_coords(pose_results)

        y16 = landmark_coords['Landmark 16'][1] if 'Landmark 16' in landmark_coords else None
        y12 = landmark_coords['Landmark 12'][1] if 'Landmark 12' in landmark_coords else None
        y11 = landmark_coords['Landmark 11'][1] if 'Landmark 11' in landmark_coords else None
        y15 = landmark_coords['Landmark 15'][1] if 'Landmark 15' in landmark_coords else None

        ybody = (y12 + y11) / 2

        check_and_rotate_hand(y16, prev_y16, pin)
        check_and_rotate_hand(y15, prev_y15, pin2)
        check_and_rotate_body(ybody, prev_ybody)

        # print(int(y16 * 480))
        # print(int(prev_y16 * 480))

        prev_y16, prev_y12, prev_y11, prev_y15, prev_ybody = y16, y12, y11, y15, ybody

        cv2.imshow('Output', frame)
    except:
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()