from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtWidgets
import os
from views.widgets.options_menu import HessianMenu, CVRidgeMenu, ScharrMenu, SobelMenu, CannyMenu, SatoMenu, MeijeringMenu, PrewittMenu, FaridMenu
from .transformation import hessian_filter, sobel_filter, scharr_filter, cv_ridge_filter, canny_edge_detection, sato_filter, meijering_filter, prewitt_filter, farid_filter
""" The QItemObject class is used to store the information about the images in the directory. 
    It is used to populate the QTreeWidget with the images. 
    Data is stored in the following format: [name, extension, path] """

class QItemObject():
    EXTENSIONS = ["PNG", "JPG", "JPEG", "GIF", "BMP"]

    def __init__(self, path: str):
        self.path = path
        self.categories = ['name', 'extension', 'path'] # the order of the information

    def __checkExtension(self):
        extension = self.__getExtension().upper()
        return extension in self.EXTENSIONS
    
    def __getExtension(self):
        return os.path.splitext(self.path)[1][1:]
        
    def __getData(self):
        filename = os.path.basename(self.path).split('.')[0]
        extension = os.path.basename(self.path).split('.')[1]
        
        return [filename, extension, self.path]
        
    def data(self):
        if self.__checkExtension():
            file_data = self.__getData()        
            return file_data
        return None


# Perform any operations on the data from Model
# First idea: three controllers:
# - ImageController
# - DirectoryController
# - EdgeMenuController

class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    @pyqtSlot(int)
    def change_amount(self, value):
        self._model.amount = value

        # calculate even or odd
        self._model.even_odd = 'odd' if value % 2 else 'even'

        # calculate button enabled state
        self._model.enable_reset = True if value else False
        
# Every logic task should be done in the controller       
# A slot is called when the signal connected to it is emmitted

# Slot is a function that is supposed to do something,
# then signals are a done thing e.g.: value_changed, button_clicked

class ImageController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
    
    @pyqtSlot(int)
    def on_tab_bar_clicked(self, index):
        # If the last tab clicked, add a new tab
        if index == self._model._image_tabs_count - 1:
            self._model.add_new_tab.emit(self._model._image_tabs_count - 1)
        print(index, self._model._image_tabs_count - 1)
        


class EdgeDetectionController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self._menus = {'sobel_button': SobelMenu,
                       'scharr_button': ScharrMenu,
                       'canny_button': CannyMenu,
                       'sato_button': SatoMenu,
                       'meijering_button': MeijeringMenu,
                       'prewitt_button': PrewittMenu,
                       'farid_button': FaridMenu,
                       'hessian_button': HessianMenu,
                       'cvridgefilter_button': CVRidgeMenu}
        
        self._filters = {'sobel_button': sobel_filter,
                         'scharr_button': scharr_filter,
                         'canny_button': canny_edge_detection,
                         'sato_button': sato_filter,
                         'meijering_button': meijering_filter,
                         'prewitt_button': prewitt_filter,
                         'farid_button': farid_filter,
                         'hessian_button': hessian_filter,
                         'cvridgefilter_button': cv_ridge_filter}
        
    @pyqtSlot(str)
    def on_button_clicked(self, button_name):
        if button_name in self._menus:
            print(f"The button has its own Menu: {button_name}.")
            class_name = self._menus.get(button_name)()
            class_name.TRANS_FUNC = self._filters.get(button_name)
            self._model.current_menu = class_name
            
            # print(type(class_name))
            # print(type(self._menus.get(button_name)()))
        else:
            print(f"The button does not have its own Menu: {button_name}.")
    
    @pyqtSlot(dict)
    def on_settings_applied(self, settings):
        self._model.current_settings = settings



class DirectoryController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
    
    @pyqtSlot(bool)
    def change_directory(self):
        # Returns a list of image objects given as {name: ..., ext: ..., path ...}
        self.folder = QtWidgets.QFileDialog.getExistingDirectory()
        if not self.folder:
            self._model.directory = ''
        else:
            self._model.directory = self.folder
    
    @pyqtSlot(str)
    def populate_list(self, directory):
        """ Populate the list with images from the directory.
            The available extensions are defined in the QItemObject class,
            which also handles the validation of the files in the directory. """
        images = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            item = QItemObject(path)
            if item.data():
                images.append(item)
        
        listItems = [QtWidgets.QTreeWidgetItem(x.data()) for x in images]
        self._model.tree_items = listItems

    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_item_clicked(self, item, column):
        # Get the path of the image
        path = item.text(2)
        self._model.current_image_path = path

    
# Controller does not know about the view 