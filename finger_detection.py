# TODO : '모바일 엣지향 손 포즈 인식 어플리케이션을 위한 인식률 향상 방법' 논문 대한 예시 코드 및 설명

# [ ] OpenCV를 활용하여 손가락을 인식하고, 인식 결과를 출력하는 코드 

import cv2
import mediapipe as mp

# Mediapipe 손 모양 인식 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# 웹캠 초기화
cap = cv2.VideoCapture(0)

def count_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    count = 0

    # 각 손가락의 끝이 손바닥 중앙보다 위에 있는지 확인
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    # 엄지손가락 확인
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        count += 1

    return count

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_count = count_fingers(frame, hand_landmarks)
            
            # 손가락 개수를 화면에 표시
            cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # 손가락 개수를 콘솔에 출력
            print(f'Fingers: {fingers_count}')

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# [ ] 인식률을 저하시키는 요인인 그림자나 얼굴에 대해 보완하는 코드 

import cv2
import mediapipe as mp

# Mediapipe 손 모양 인식 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Haar Cascade 얼굴 인식 초기화
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 웹캠 초기화
cap = cv2.VideoCapture(0)

def count_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    count = 0

    # 각 손가락의 끝이 손바닥 중앙보다 위에 있는지 확인
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    # 엄지손가락 확인
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        count += 1

    return count

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 인식 및 마스킹
    faces = face_cascade.detectMultiScale(frame_gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), -1)
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_count = count_fingers(frame, hand_landmarks)
            
            # 손가락 개수를 화면에 표시
            cv2.putText(frame, f'Fingers: {fingers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # 손가락 개수를 콘솔에 출력
            print(f'Fingers: {fingers_count}')

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''
그림자나 얼굴과 같은 배경 요소가 손 모양 인식에 영향을 주는 이유는 컴퓨터 비전 시스템이 이러한 요소를 손으로 잘못 인식하거나 손의 일부로 인식할 수 있기 때문입니다. Mediapipe와 같은 손 인식 알고리즘은 이미지의 픽셀 정보를 기반으로 작동하기 때문에, 배경에 있는 복잡한 요소가 인식의 정확도를 저하시킬 수 있습니다. 아래는 이러한 요소가 인식률에 영향을 주는 몇 가지 이유입니다:

1. 잘못된 검출
그림자나 얼굴과 같은 배경 요소가 손의 일부로 잘못 인식될 수 있습니다. 특히 그림자는 손의 모양과 유사한 형태를 만들 수 있으며, 얼굴의 피부색이 손의 피부색과 유사하다면 손으로 잘못 인식될 가능성이 있습니다.

2. 잡음(Noise)
배경 요소가 잡음으로 작용하여 손의 랜드마크 검출을 방해할 수 있습니다. 손의 랜드마크를 정확하게 검출해야 손가락 개수를 올바르게 세울 수 있는데, 배경 잡음이 많으면 랜드마크 검출의 정확도가 떨어집니다.

3. 추적 오류
동영상 스트림에서 손을 추적할 때 배경 요소가 손과 겹치거나 비슷한 모양을 가지면 추적이 어려워질 수 있습니다. 예를 들어, 얼굴이 손과 겹치거나 그림자가 손 모양을 왜곡하면 추적 알고리즘이 혼란스러워집니다.

4. 색상 혼동
얼굴이나 그림자의 색상이 손의 피부색과 유사할 경우, 색상 기반 필터링 기법이 효과적으로 작동하지 않을 수 있습니다. 이로 인해 손 이외의 부분이 손으로 잘못 인식될 수 있습니다.

해결 방법
이러한 문제를 해결하기 위해 몇 가지 방법을 사용할 수 있습니다:

배경 제거

배경 제거 알고리즘을 사용하여 손 외의 모든 배경을 제거합니다.
python
코드 복사
fgbg = cv2.createBackgroundSubtractorMOG2()
fgmask = fgbg.apply(frame)
얼굴 마스킹

Haar Cascade 또는 딥러닝 기반 얼굴 검출기를 사용하여 얼굴을 검출하고 마스킹합니다.
python
코드 복사
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(frame_gray, 1.1, 4)
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), -1)
밝기 및 대비 조정

이미지의 밝기와 대비를 조정하여 그림자를 줄입니다.
python
코드 복사
frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=30)
색상 필터링

특정 색상 범위를 필터링하여 손만 검출합니다.

'''