import websocket
import _thread
import time
import cv2
import numpy as np

host = "donkeycar"
port = 8887

socket_address = f"ws://gopher:8887/wsDrive"
video_address = f"http://gopher:8887/video"


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        # your car logic here
        print("inside onOpen")
        cap = cv2.VideoCapture(video_address)

        ret, frame = cap.read()
        height = frame.shape[0]
        width = frame.shape[1]

        while True:
            ret, frame = cap.read()
            # do something based on the frame
            angle = 0.0
            throttle = 0.2
            message = f"{{\"angle\":{angle},\"throttle\":{throttle},\"drive_mode\":\"user\",\"recording\":false}}"
            ws.send(message)
            print(message)

            # detectLane(frame)
            blackWhiteFrame = blur(frame)

            cv2.imshow('Frame', frame)
            cv2.imshow('BW', blackWhiteFrame)

            # when detecting white lines
            # getLane()

            # stop the car
            if cv2.waitKey(1) == 27:
                throttle = 0
                message = f"{{\"angle\":{angle},\"throttle\":{throttle},\"drive_mode\":\"user\",\"recording\":false}}"
                ws.send(message)
                break

    _thread.start_new_thread(run, ())


def blur(frame):
    bw = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(bw, (5, 5), 0)
    newCanny = cv2.Canny(blur, 60, 180)
    return newCanny


def thresholding(img):

    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([80, 0, 0])
    upperWhite = np.array([255, 160, 255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    return maskWhite


# def detectLane(frame):

    #imgThres = thresholding(frame)
    #cv2.imshow('Thres', imgThres)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket_address,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
