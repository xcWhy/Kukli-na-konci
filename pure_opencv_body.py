import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def get_landmark_coords(pose_results):
    landmark_coords = {}
    for i, landmark in enumerate(pose_results.pose_landmarks.landmark):
        landmark_coords[f"Landmark {i}"] = (landmark.x, landmark.y)
    return landmark_coords

prev_y16, prev_y12, prev_y11, prev_y15 = None, None, None, None


while True:
    # read frame
    ret, frame = cap.read()

    #frame = cv2.resize(frame, (350, 600))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(frame_rgb)

    mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    landmark_coords = get_landmark_coords(pose_results)

    y16 = landmark_coords['Landmark 16'][1]
    y12 = landmark_coords['Landmark 12'][1]
    y11 = landmark_coords['Landmark 11'][1]
    y15 = landmark_coords['Landmark 15'][1]

    # check if y-coordinate is changing or staying the same
    if prev_y16 is not None:
        if y16 is not None and abs(y16 - prev_y16) <= 0.03:
            print('Landmark 16 Y-coordinate is staying the same')
        else:
            print('Landmark 16 Y-coordinate is changing')
    if prev_y12 is not None:
        if y12 is not None and abs(y12 - prev_y12) <= 0.03:
            print('Landmark 12 Y-coordinate is staying the same')
        else:
            print('Landmark 12 Y-coordinate is changing')
    if prev_y11 is not None:
        if y11 is not None and abs(y11 - prev_y11) <= 0.03:
            print('Landmark 11 Y-coordinate is staying the same')
        else:
            print('Landmark 11 Y-coordinate is changing')
    if prev_y15 is not None:
        if y15 is not None and abs(y15 - prev_y15) <= 0.03:
            print('Landmark 15 Y-coordinate is staying the same')
        else:
            print('Landmark 15 Y-coordinate is changing')


    prev_y16, prev_y12, prev_y11, prev_y15 = y16, y12, y11, y15

    cv2.imshow('Output', frame)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()