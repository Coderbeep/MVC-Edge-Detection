from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage
import cv2
import os
import numpy as np
from functools import singledispatchmethod

class ImageViewer(QtWidgets.QGraphicsView):
    itemsDropped = QtCore.pyqtSignal(QtCore.QMimeData)
    imageSet = QtCore.pyqtSignal(str)
    
    def __init__(self, graphicsView: QtWidgets.QGraphicsView = None):
        super(ImageViewer, self).__init__(graphicsView)
        
        self.setupView()
        self.setupFormatting()
        
        self.image = None
        self.path = None
        self.filled = False
        self.scene = QtWidgets.QGraphicsScene()
        self.pan_margin = 1000
        
        self.setAcceptDrops(True)
        self.dragEnterEvent = self.dragEnterEvent
        self.dragMoveEvent = self.dragMoveEvent
        self.dropEvent = self.dropEvent
        
        self.zoom_level = 0
        self.zoom_limits = [-8, 8]
        
        self.contextMenuEvent = self.contextMenuEvent

    def setupView(self):
        self.setInteractive(True)
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def setupFormatting(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Stylesheet
        self.setStyleSheet(
            "QMenu {\n"
            "            padding: 0px;\n"
            "            border: 1px solid black;\n"
            "}\n"
            "QMenu::item {\n"
            "            background-color: palette(button);\n"
            "        }\n"
            "QMenu::item:selected {\n"
            "            background-color: lightgray;\n"
            "}"
        )
        self.setLineWidth(0)
        
    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        contextMenu = QtWidgets.QMenu(self)

        closeAction = contextMenu.addAction("Close")
        zoomInAction = contextMenu.addAction("Zoom in")
        zoomOutAction = contextMenu.addAction("Zoom out")
        
        # TODO: function to handle 
        closeAction.triggered.connect(lambda: print("Close action")) 
        zoomInAction.triggered.connect(lambda: print("Zoom in action"))
        zoomOutAction.triggered.connect(lambda: print("Zoom out action"))
        
        contextMenu.exec(self.mapToGlobal(event.pos()))
    
    @singledispatchmethod
    def loadImage(self, path_or_image):
        raise NotImplementedError("Unsupported input type.")

    @loadImage.register(np.ndarray)
    def _1(self, numpy_img):
        shape = numpy_img.shape
        height, width = shape[0], shape[1]
        
        if len(shape) == 2: # the image is in grayscale
            bytes_per_line = width
            q_image = QImage(numpy_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else: # colored image
            bytes_per_line = 3 * width
            q_image = QImage(numpy_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        panning_pixmap = QtGui.QPixmap(width + 2 * self.pan_margin, height + 2 * self.pan_margin)
        panning_pixmap.fill(QtCore.Qt.transparent)
        
        painter = QtGui.QPainter(panning_pixmap)
        painter.drawImage(QtCore.QPoint(self.pan_margin, self.pan_margin), q_image)
        painter.end()
        
        self.scene.addPixmap(panning_pixmap)
        self.setScene(self.scene)
        self.image = numpy_img
        self.filled = True

    def getFilename(self, path):
        return os.path.basename(path)

    @loadImage.register(str)
    def _2(self, path):
        '''Read the image in OpenCV2'''
        self.scene.clear()
        self.image = cv2.imread(path)
        self.path = path
        shape = self.image.shape
        height, width = shape[0], shape[1]
        bytes_per_line = 3 * width

        q_image = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        panning_pixmap = QtGui.QPixmap(width + 2 * self.pan_margin, height + 2 * self.pan_margin)
        panning_pixmap.fill(QtCore.Qt.transparent)
        
        painter = QtGui.QPainter(panning_pixmap)
        painter.drawImage(QtCore.QPoint(self.pan_margin, self.pan_margin), q_image)
        painter.end()
        
        self.scene.addPixmap(panning_pixmap)
        self.setScene(self.scene)
        self.filled = True
        self.imageSet.emit(self.getFilename(self.path))
        
        
    def wheelEvent(self, event: QtGui.QWheelEvent):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            scroll_in = event.angleDelta().y() > 0
            zoom_factor = 1.25 if scroll_in else 0.8
            
            if (scroll_in and self.zoom_level < self.zoom_limits[1] or not scroll_in and self.zoom_level > self.zoom_limits[0]):
                self.scale(zoom_factor, zoom_factor)
                self.zoom_level += 1 if scroll_in else -1
        else:
            QtWidgets.QGraphicsView.wheelEvent(self, event)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.itemsDropped.emit(event.mimeData())
        else:
            event.ignore()
            
    def onTransformClick(self, settings):
        if self.filled:
            func = settings.get('function')
            del settings['function']
            self.image = func(self.image, **settings)
            self.loadImage(self.image)