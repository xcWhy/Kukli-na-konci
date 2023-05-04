import cv2
import mediapipe as mp

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


def check_and_rotate_hand(coord, prev_coord):
    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.05:
            print('something is NOT moving !!!')

        elif coord is not None and prev_coord is not None and coord > prev_coord:
            print('something is moving up')

        elif coord is not None and prev_coord is not None and coord < prev_coord:
            print('something is moving down')


def check_and_rotate_body(coord, prev_coord):
    global pin, pin2, pin3

    if prev_coord is not None:
        if coord is not None and abs(coord - prev_coord) <= 0.05:
            print('body is NOT moving !!!')


        elif coord is not None and prev_coord is not None and coord > prev_coord:
            print('body is moving up')


        elif coord is not None and prev_coord is not None and coord < prev_coord:
            print('body is moving down')


while True:

    # read frame
    ret, frame = cap.read()

    # frame = cv2.resize(frame, (350, 600))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(frame_rgb)

    mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    landmark_coords = get_landmark_coords(pose_results)

    y16 = landmark_coords['Landmark 16'][1] if 'Landmark 16' in landmark_coords else None
    y12 = landmark_coords['Landmark 12'][1] if 'Landmark 12' in landmark_coords else None
    y11 = landmark_coords['Landmark 11'][1] if 'Landmark 11' in landmark_coords else None
    y15 = landmark_coords['Landmark 15'][1] if 'Landmark 15' in landmark_coords else None

    print(y16)

    if y12 is not None and y11 is not None:
        ybody = (y12 + y11) / 2

        check_and_rotate_hand(y16, prev_y16)
        check_and_rotate_hand(y15, prev_y15)
        check_and_rotate_body(ybody, prev_ybody)

        # print(int(y16 * 480))
        # print(int(prev_y16 * 480))

        prev_y16, prev_y12, prev_y11, prev_y15, prev_ybody = y16, y12, y11, y15, ybody

    cv2.imshow('Output', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()