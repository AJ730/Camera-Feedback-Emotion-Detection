import os

import cv2
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Detector:
    def __init__(self, model, ):
        self.model = model
        self.model.load_weights("facedetection/emotion_detection/model.h5")
        self.emotions = []

    def capture(self):

        # prevents openCL usage and unnecessary logging messages
        cv2.ocl.setUseOpenCL(False)

        # dictionary which assigns each label an emotion (alphabetical order)
        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        # start the webcam feed
        cap = cv2.VideoCapture(0)

        while True:
            # Find haar cascade to draw bounding box around face
            ret, frame = cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = self.model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                # cv2.putText(frame, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                #             (255, 255, 255), 2, cv2.LINE_AA)

                self.emotions.append(str(emotion_dict[maxindex]))

            # cv2.imshow('Video', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # def send_signal():
            #     c = Counter(self.emotions )
            #
            #     if len(c) > 0:
            #         value, count = c.most_common()[0]
            #         if value not in [ "Neutral, Surprised"]:
            #             # self.sc.send_message(value)
            #             self.emotions.clear()
            #             self.emotions.append("Neutral")
            #
            # t = RepeatedTimer(10, send_signal)

        cap.release()
        cv2.destroyAllWindows()
        # t.stop()
