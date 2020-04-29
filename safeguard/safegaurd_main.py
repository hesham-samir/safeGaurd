import sys
from os import path


from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from face_detection_widget import MainFaceDetectioWidget

def main(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    tab_window = QtWidgets.QTabWidget()
    touch_face_detection_widget = MainFaceDetectioWidget(haar_cascade_filepath)
    mask_detection = QtWidgets.QWidget()
    tab_window.addTab(touch_face_detection_widget,"Touch Face Detection")
    tab_window.addTab(mask_detection,"Mask Detection")
    main_window.setCentralWidget(tab_window)
    main_window.showMaximized()

    tb = main_window.addToolBar("Tools")
    tb.addAction("Touch Face Detection")
    tb.addAction("Mask Detection")
    tb.addAction("About")
    tb.setMovable(False)
    #tb.setFixedWidth(200);


#    palette = QtGui.QPalette()
#    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(3, 18, 14))
#    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
#    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
#    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
#    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
#    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
#    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
#    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
#    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
#    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
#    app.setPalette(palette)

    sys.exit(app.exec_())


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join('.\\haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)
