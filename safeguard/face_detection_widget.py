import cv2
import numpy as np
import winsound         # for sound
import time             # for sleep



from utils import detector_utils as detector_utils
import tensorflow as tf
import argparse

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from record_video import RecordVideo

from PyQt5.QtCore import qDebug

class FaceDetectionWidget(QtWidgets.QWidget):

    def __init__(self, haar_cascade_filepath, parent=None):
        ###############################Face initialization#######################
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (50, 50)
        self.l1 = QtWidgets.QLabel()
        ###############################Hand initialization#######################
        self. detection_graph, self.sess = detector_utils.load_inference_graph()

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)
        faces = self.classifier.detectMultiScale(gray_image,scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=(self._min_size))

        for (x, y, w, h) in faces:
            cv2.rectangle(image,(x, y),(x+w, y+h), self._red,self._width)
        ####################### hand ####################
        try:
            image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        boxes, scores = detector_utils.detect_objects(image_np,
                                                     self. detection_graph,
                                                     self.sess)

        # draw bounding boxes on frame
        detector_utils.draw_box_on_image(2, 0.5,
                                         scores, boxes, 320, 180,
                                         image)
        touched = False
        for (x, y, w, h) in faces:
            for i in range(0,1):
#                qDebug("********Face********")
#                qDebug(str(x))
#                qDebug(str(y))
#                qDebug(str(x+w))
#                qDebug(str(y+h))
#                qDebug("########Hand########")
#                qDebug(str(boxes[i][1]*320))
#                qDebug(str(boxes[i][0]*180))
#                qDebug(str(boxes[i][3]*320))
#                qDebug(str(boxes[i][2]*180))
#                qDebug(str(scores[i]))
#                qDebug(str(self.isTouching(x,y,x+w,y+h,boxes[i][1]*320,boxes[i][0]*180,boxes[i][3]*320,boxes[i][2]*180)))

                if self.isTouching(x,y,x+w,y+h,boxes[i][0]*320,boxes[i][1]*180,boxes[i][2]*320,boxes[i][3]*180) and scores[i] > 0.5:
                    touched = True

        if touched:
            winsound.Beep(440, 50) # frequency, duration


        #################################################

        self.image = self.get_qimage(image)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def isTouching(self,minx1,miny1, maxx1, maxy1, minx2,miny2, maxx2, maxy2):

        # If one rectangle is on left side of other
        if(minx1 >= maxx2 or minx2 >= maxx1):
            return False

        # If one rectangle is above other
        if(miny1 >= maxy2 or miny2 >= maxy1):
            return False

        return True


class MainFaceDetectioWidget(QtWidgets.QWidget):
    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp)

        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.detect_faces
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)
