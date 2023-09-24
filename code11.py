from threading import Thread
import random
import cv2
import face_recognition
import numpy as np
import playsound
from scipy.spatial import distance as dist

MIN_AER = 0.30
EYE_AR_CONSEC_FRAMES = 10


COUNTER = 0


def check_engine(ce_file):
    playsound(ce_file)

def battery(b_file):
    playsound(b_file)

def abs(ab_file):
    playsound(ab_file)

def overheat(oh_file):
    playsound(oh_file)

def oil(o_file):
    playsound(o_file)

def warning(symbol):

    ENGINE_ON = False
    BATTERY_ON = False
    ABS_ON = False
    HEAT_ON = False
    OIL_ON = False

    if symbol == 0:

        if not ENGINE_ON:

            ENGINE_ON = True
            t = Thread(target=check_engine,
                       args=('C:/Users/LavUsh/Desktop/pbl/DD/engine.wav',))
            t.deamon = True
            t.start()

        else:

            ENGINE_ON = False

    if symbol == 1:

        if not BATTERY_ON:

            BATTERY_ON = True
            t = Thread(target=battery,
                       args=('C:/Users/LavUsh/Desktop/pbl/DD/battery.wav',))
            t.deamon = True
            t.start()

        else:

            BATTERY_ON = False

    if symbol == 2:

        if not ABS_ON:

            ABS_ON = True
            t = Thread(target=abs,
                       args=('C:/Users/LavUsh/Desktop/pbl/DD/abs.wav',))
            t.deamon = True
            t.start()

        else:

            ABS_ON = False

    if symbol == 3:

        if not HEAT_ON:

            HEAT_ON = True
            t = Thread(target=overheat,
                       args=('C:/Users/LavUsh/Desktop/pbl/DD/overheat.wav',))
            t.deamon = True
            t.start()

        else:

            HEAT_ON = False

    if symbol == 4:

        if not OIL_ON:

            OIL_ON = True
            t = Thread(target=oil,
                       args=('C:/Users/LavUsh/Desktop/pbl/DD/oil.wav',))
            t.deamon = True
            t.start()

        else:

            OIL_ON = False


def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear


def sound_alarm(alarm_file):

    playsound(alarm_file)

def main():
    global COUNTER
    count = 0
    ALARM_ON = False
    video_capture = cv2.VideoCapture(0)
    symbol = random.randint(0, 4)

    while True:

        ret, frame = video_capture.read(0)

        count = count + 1

        if count < 2:
            warning(symbol)

        face_landmarks_list = face_recognition.face_landmarks(frame)

        for face_landmark in face_landmarks_list:
            leftEye = face_landmark['left_eye']
            rightEye = face_landmark['right_eye']

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2

            lpts = np.array(leftEye)
            rpts = np.array(rightEye)

            cv2.polylines(frame, [lpts], True, (255, 255, 0), 1)
            cv2.polylines(frame, [rpts], True, (255, 255, 0), 1)

            if ear < MIN_AER:
                COUNTER += 1

                if COUNTER >= EYE_AR_CONSEC_FRAMES:

                    if not ALARM_ON:
                        ALARM_ON = True
                        t = Thread(target=sound_alarm,
                                   args=('C:/Users/LavUsh/Desktop/pbl/DD/alarm.mp3',))
                        t.deamon = True
                        t.start()

                    cv2.putText(frame, "ALERT! You are falling asleep!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            else:
                COUNTER = 0
                ALARM_ON = False

            cv2.putText(frame, "EAR: {:.2f}".format(ear), (500, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),2)

            cv2.putText(frame, str(symbol), (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Sleep detection program.", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
