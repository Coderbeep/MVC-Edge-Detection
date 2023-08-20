from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.main_view_ui import Ui_MainWindow
from controllers.main_ctrl import DirectoryController, ImageController, EdgeDetectionController
from PyQt5 import QtWidgets, QtGui
from views.widgets.image_viewer import ImageViewer
import cv2
import numpy as np

def sobel_filter(image, kernel_size=3, direction="combined"):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        convolved = None
        match direction:
            case "combined":
                sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
                sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)

                gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
                gradient_magnitude = cv2.normalize(
                    gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
                )
                convolved = gradient_magnitude

            case "vertical":
                sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
                sobel_x = cv2.normalize(sobel_x, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                convolved = sobel_x

            case "horizontal":
                sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
                sobel_y = cv2.normalize(sobel_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                convolved = sobel_y

        filtered_image = convolved
        return filtered_image
# How to use:
# - connect widgets to controller
# - listen for model event signals
# - this is supposed to have access to the widget names

MENU_BUTTONS = ['canny_button', 
                'sobel_button', 
                'scharr_button', 
                'sato_button', 
                'meijering_button', 
                'prewitt_button', 
                'farid_button', 
                'hessian_button', 
                'cvridgefilter_button',
                'frangi_button']

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        # Models
        self._model = model
        
        # Controllers
        self._directory_controller = DirectoryController(self._model)
        self._image_controller = ImageController(self._model)
        self._edge_detection_controller = EdgeDetectionController(self._model)
        
        # UIs
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # 1. Connect widgets to their controllers
        self._ui.open_dir_button.clicked.connect(self._directory_controller.change_directory)
        self._ui.image_viewer_tabs.tabBarClicked.connect(self._image_controller.on_tab_bar_clicked)
        self._ui.image_list.itemClicked.connect(self._directory_controller.on_item_clicked)
        for button_name in MENU_BUTTONS:
            button = getattr(self._ui, button_name)
            button.clicked.connect(lambda _, name=button_name: self._edge_detection_controller.on_button_clicked(name))
        
        # 2. Listen to the model signals
        self._model.directory_changed.connect(self._directory_controller.populate_list)
        self._model.tree_items_changed.connect(self.on_tree_items_changed) 
        self._model.add_new_tab.connect(self.add_new_tab)
        self._model.current_path_changed.connect(self.on_current_path_changed)
        self._model.current_menu_changed.connect(self.on_current_menu_changed)
        self._model.settings_changed.connect(self.on_settings_changed)
        
        self.apply_default_settings()

    def apply_default_settings(self):
        self._ui.image_viewer_tabs.removeTab(0)
        self.add_new_tab(0)
        self._ui.image_viewer_tabs.setCurrentIndex(0)
        
        # TODO: remove that before github upload
        self._model.directory = 'C:/Users/jakub/Desktop'
    
    @pyqtSlot(dict)
    def on_settings_changed(self, settings):
        current_viewer = self._ui.image_viewer_tabs.currentWidget().children()[1]
        current_image = current_viewer.image
        func = self._model.current_menu.TRANS_FUNC
        transformed_image = func(current_image, **settings)
        current_viewer.loadImage(transformed_image)
        

    @pyqtSlot(QtWidgets.QWidget)
    def on_current_menu_changed(self, instance):
        stacked_widget = self._ui.stackedWidget
        current_menu = instance   
        stacked_widget.insertWidget(0, current_menu)
        stacked_widget.setCurrentIndex(0)
        self._model.current_apply_button = instance.applyButton
        instance.settingsApplied.connect(self._edge_detection_controller.on_settings_applied)
        pass
        

    @pyqtSlot(list)
    def on_tree_items_changed(self, items):
        for item in items:
            item.setIcon(0, QtGui.QIcon(item.data(2,0)))
            self._ui.image_list.addTopLevelItem(item)
    
    @pyqtSlot(int)
    def add_new_tab(self, index):
        new_tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(new_tab)
        
        image_viewer = ImageViewer()
        layout.addWidget(image_viewer)
        
        self._ui.image_viewer_tabs.insertTab(index, new_tab, 'New Tab')
        self._model.image_tabs_count += 1
        
    @pyqtSlot(str)
    def on_current_path_changed(self, path):
        current_viewer = self._ui.image_viewer_tabs.currentWidget().children()[1]
        current_viewer.loadImage(path)