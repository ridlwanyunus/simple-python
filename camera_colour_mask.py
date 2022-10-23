import cv2

min_blue, min_green, min_red = 45, 0, 0
max_blue, max_green, max_red = 255, 255, 99

v = cv2.__version__.split('.')[0]

class VideoMask(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        _, frame_BGR = self.video.read()

        frame_HSV = cv2.cvtColor(frame_BGR, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(
            frame_HSV,
            (min_blue, min_green, min_red),
            (max_blue, max_green, max_red)
        )

        if v == '3':
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        else:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if contours:
            (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
            cv2.rectangle(
                frame_BGR,
                (x_min - 15, y_min - 15),
                (x_min + box_width + 15, y_min + box_height + 15),
                (0, 255, 0),
                3
            )

            label = 'Vaseline'

            cv2.putText(
                frame_BGR,
                label,
                (x_min - 5, y_min - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (0, 255, 0),
                2
            )



        ret, jpg = cv2.imencode('.jpg', frame_BGR)
        return jpg.tobytes()
