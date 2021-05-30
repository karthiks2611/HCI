import mediapipe as mp
import cv2


class HandDetection:
    def __init__(self):
        self.mode = False
        self.maxHands = 1
        self.detectionConfidence = 0.8
        self.trackConfidence = 0.8

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.mp_hand = mp.solutions.hands

        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=self.detectionConfidence,
                                                  min_tracking_confidence=self.trackConfidence)
        self.hands = self.mp_hand.Hands(max_num_hands=self.maxHands, min_tracking_confidence=self.detectionConfidence,
                                        min_detection_confidence=self.trackConfidence)
        self.results = None

    def detect(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if self.results.multi_hand_landmarks:
            # print(results.multi_hand_landmarks)
            # Left Hand
            # mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Right Hand
            for handLms in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, handLms, self.mp_hand.HAND_CONNECTIONS,
                                               self.mp_drawing.DrawingSpec(color=(0, 0, 255),
                                                                           thickness=2, circle_radius=4),
                                               self.mp_drawing.DrawingSpec(color=(0, 255, 255),
                                                                           thickness=2, circle_radius=2))

        return frame

    def positions(self, img, hand_no=0):
        pt_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for i, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                pt_list.append([i, cx, cy])

        return pt_list
