import threading
from collections import Counter
import eventlet
import socketio
from facedetection.emotion_detection.detection import Detector
from facedetection.model.model import getModel

#
# class SocketStream(threading.Thread):
#     def __init__(self, host, port, clients):
#         super().__init__()
#         self.conn = None
#         self.host = host
#         self.port = port
#
#         soc = socket.socket()
#         soc.bind((host, port))
#         soc.listen(clients)
#         self.soc = soc
#         print("server started")
#
#     def listen(self):
#         # Establish connection with client.
#         conn, addr = self.soc.accept()
#         self.conn = conn
#         print("client:" + str(addr) + " connected!")
#
#     def send(self, message):
#         self.conn.send(bytes(message + "\r\n", 'UTF-8'))
#


#
# class sc:
#
#     def __init__(self):
#         self.sio = socketio.Server()
#         self.app = socketio.WSGIApp(   self.sio, static_files={
#             '/': {'content_type': 'text/html', 'filename': 'index.html'}
#         })
#
#
#     def start_server(self):
#         sio = self.sio
#
#         @sio.event
#         def connect(sid, string):
#             print('connect ', sid)
#
#         @sio.event
#         def disconnect(sid):
#             print('disconnect ', sid)
#
#         @sio.event
#         def request(sid, data):
#             if (data):
#                 print("received")
#                 sio.emit("emotion", "sad")
#
#         print("Server started")
#         eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), self.app)
#
#
#     def send_message(self, msg):
#         self.sio.emit("emotion",msg)
#

class CameraFeedback:

    def __init__(self):
        self.detector = Detector(getModel())

    def send_stream(self):
        self.detector.capture()


if __name__ == '__main__':
    c = CameraFeedback()


    def task():
        sio = socketio.Server()
        app = socketio.WSGIApp(sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })

        @sio.event
        def connect(sid, string):
            print('connect ', sid)

        @sio.event
        def disconnect(sid):
            print('disconnect ', sid)

        @sio.event
        def request(sid, data):
            if (data):
                emotions = c.detector.emotions
                counter = Counter(emotions)

                if len(emotions) > 0:
                    value, count = counter.most_common()[0]
                    if value not in [ "Neutral", "Surprised"]:
                    # self.sc.send_message(value)
                        print(c.detector.emotions)
                        c.detector.emotions.clear()
                        sio.emit("emotion", value)



        print("Server started")
        eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)


    thread = threading.Thread(target=task)
    thread.start()

    c.send_stream()
