from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets

# Contains signals
# Contains data 
# Getters and setters for the data


class Model(QObject):
    directory_changed = pyqtSignal(str)
    tree_items_changed = pyqtSignal(list)
    
    add_new_tab = pyqtSignal(int)
    tabs_count_changed = pyqtSignal(int)
    current_path_changed = pyqtSignal(str)

    current_menu_changed = pyqtSignal(QtWidgets.QWidget)
    current_apply_button_changed = pyqtSignal()
    settings_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        # Directory selection
        self._directory = ''
        self._tree_items = []
        self._current_image_path = ''
        
        # Tabs images
        self._current_image_tab_index = 0
        self._image_tabs_count = 1
        self._current_image = None
        
        # Menu properties
        self._current_menu = None
        self._current_apply_button = None    
        self._current_transformation = None
        self._current_settings = None

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value
        self.directory_changed.emit(value)
    
    @property
    def tree_items(self):
        return self._tree_items
    
    @tree_items.setter
    def tree_items(self, value):
        self._tree_items = value
        self.tree_items_changed.emit(value)
        
    @property
    def current_image_tab_index(self):
        return self._current_image_tab_index
    
    @current_image_tab_index.setter
    def current_image_tab_index(self, index):
        self._current_image_tab_index = index

    @property
    def image_tabs_count(self):
        return self._image_tabs_count
    
    @image_tabs_count.setter
    def image_tabs_count(self, value):
        self._image_tabs_count = value
        self.tabs_count_changed.emit(value)
    
    @property
    def current_image(self):
        return self._current_image
    
    @current_image.setter
    def current_image(self, value):
        self._current_image = value
    
    @property
    def current_image_path(self):
        return self._current_image_path
    
    @current_image_path.setter
    def current_image_path(self, value):
        self._current_image_path = value
        self.current_path_changed.emit(value)
        
    @property
    def current_menu(self):
        return self._current_menu
    
    @current_menu.setter
    def current_menu(self, value):
        self._current_menu = value
        self.current_menu_changed.emit(value)
        
    @property
    def current_apply_button(self):
        return self._current_apply_button
    
    @current_apply_button.setter
    def current_apply_button(self, button):
        self._current_apply_button = button
        self.current_apply_button_changed.emit()
    
    @property
    def current_transformation(self):
        return self._current_transformation
    
    @current_transformation.setter
    def current_transformation(self, value):
        self._current_transformation = value
        
    @property
    def current_settings(self):
        return self._current_settings
    
    @current_settings.setter
    def current_settings(self, value):
        self._current_settings = value
        self.settings_changed.emit(value)