from PyQt5 import QtWidgets, QtCore
from .range_slider import RangeSlider

WIDGET_TYPES = [QtWidgets.QSlider, QtWidgets.QCheckBox, QtWidgets.QGroupBox, QtWidgets.QRadioButton]  

class MenuInterface(QtWidgets.QWidget):
    settingsApplied = QtCore.pyqtSignal(dict)
    APPLY_BUTTON = ''
    TRANS_FUNC = None
    
    def __init__(self):
        super().__init__()
    
    def onApplyClick(self):
        self.settingsApplied.emit(self.getSettings())
        
    def connectEvents(self):
        self.applyButton = self.findChild(QtWidgets.QPushButton, self.APPLY_BUTTON)
        self.applyButton.clicked.connect(self.onApplyClick)
    
    def getSettings(self):
        pass
  
class HessianMenu(MenuInterface):
    APPLY_BUTTON = 'apply_hessian_button'
    widgets = {'sigmas': 'sigma_value_slider',
               'black_ridges': 'black_ridges_checkbox'}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = child.value()
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()            
        
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Gaussian Standard Deviation + Labels
        self.sigma_label = QtWidgets.QLabel()
        self.sigma_label.setText('Sigma range')
        self.sigma_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.sigma_label)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        
        
        self.kernel_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.kernel_size_slider.setMinimumHeight(30)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(10)
        self.kernel_size_slider.setSliderPosition(1)
        self.kernel_size_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.kernel_size_slider.setTickInterval(1)
        self.kernel_size_slider.setObjectName('sigma_value_slider')
        self.layout.addWidget(self.kernel_size_slider)
        
        self.black_ridges_checkbox = QtWidgets.QCheckBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.black_ridges_checkbox.sizePolicy().hasHeightForWidth())
        self.black_ridges_checkbox.setSizePolicy(sizePolicy)
        self.black_ridges_checkbox.setObjectName("black_ridges_checkbox")
        self.black_ridges_checkbox.setText("Black ridges")
        self.layout.addWidget(self.black_ridges_checkbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_hessian_button')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
      
class CVRidgeMenu(MenuInterface):
    APPLY_BUTTON = 'apply_cvr_button'
    widgets = {}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
        
        
    def getSettings(self):
        settings = {}
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_cvr_button')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class ScharrMenu(MenuInterface):
    APPLY_BUTTON = 'apply_scharr_button'
    widgets = {'direction': 'dim_groupbox'}
    
    KERNELS = {1: 3, 2: 5, 3: 7}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = self.KERNELS[child.value()]
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()
                    if isinstance(child, QtWidgets.QGroupBox):
                        radio_buttons = [x for x in child.children() if isinstance(x, QtWidgets.QRadioButton)]
                        for radio_button in radio_buttons:
                            if radio_button.isChecked():
                                settings['direction'] = radio_button.text().lower()
                    
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # QRadioButton GroupBox
        self.dim_groupbox = QtWidgets.QGroupBox()
        self.dim_groupbox.setTitle("")
        self.dim_groupbox.setObjectName("dim_groupbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dim_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.combined_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.combined_button.setChecked(True)
        self.combined_button.setText("Combined")
        self.combined_button.setObjectName("combined_button")
        self.gridLayout_3.addWidget(self.combined_button, 0, 0, 1, 1)
        self.vertical_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.vertical_button.setText("Vertical")
        self.vertical_button.setObjectName("vertical_button")
        self.gridLayout_3.addWidget(self.vertical_button, 0, 1, 1, 1)
        self.horizontal_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.horizontal_button.setText("Horizontal")
        self.horizontal_button.setObjectName("horizontal_button")
        self.gridLayout_3.addWidget(self.horizontal_button, 0, 2, 1, 1)
        self.layout.addWidget(self.dim_groupbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_scharr_button')
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
    
class SobelMenu(MenuInterface):
    APPLY_BUTTON = 'apply_sobel_button'
    widgets = {'kernel_size': 'kernel_size_slider', 
               'direction': 'dim_groupbox'}
    KERNELS = {1: 3, 2: 5, 3: 7}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
        
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = self.KERNELS[child.value()]
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()
                    if isinstance(child, QtWidgets.QGroupBox):
                        radio_buttons = [x for x in child.children() if isinstance(x, QtWidgets.QRadioButton)]
                        for radio_button in radio_buttons:
                            if radio_button.isChecked():
                                settings['direction'] = radio_button.text().lower()
                    
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Gaussian Standard Deviation + Labels
        self.sobel_label = QtWidgets.QLabel()
        self.sobel_label.setText('Sobel Kernel Size')
        self.sobel_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.sobel_label)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.label1 = QtWidgets.QLabel()
        self.label1.setText('3')
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        
        self.label2 = QtWidgets.QLabel()
        self.label2.setText('5')
        self.label2.setSizePolicy(sizePolicy)
        self.label2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label2, 0, 1, 1, 1)
        
        self.label3 = QtWidgets.QLabel()
        self.label3.setText('7')
        self.label3.setSizePolicy(sizePolicy)
        self.label3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label3, 0, 2, 1, 1)
        self.layout.addLayout(self.gridLayout)
        
        self.kernel_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.kernel_size_slider.setMinimumHeight(30)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(3)
        self.kernel_size_slider.setSliderPosition(1)
        self.kernel_size_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.kernel_size_slider.setTickInterval(1)
        self.kernel_size_slider.setObjectName('kernel_size_slider')
        self.layout.addWidget(self.kernel_size_slider)
        
        # QRadioButton GroupBox
        self.dim_groupbox = QtWidgets.QGroupBox()
        self.dim_groupbox.setTitle("")
        self.dim_groupbox.setObjectName("dim_groupbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dim_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.combined_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.combined_button.setChecked(True)
        self.combined_button.setText("Combined")
        self.combined_button.setObjectName("combined_button")
        self.gridLayout_3.addWidget(self.combined_button, 0, 0, 1, 1)
        self.vertical_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.vertical_button.setText("Vertical")
        self.vertical_button.setObjectName("vertical_button")
        self.gridLayout_3.addWidget(self.vertical_button, 0, 1, 1, 1)
        self.horizontal_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.horizontal_button.setText("Horizontal")
        self.horizontal_button.setObjectName("horizontal_button")
        self.gridLayout_3.addWidget(self.horizontal_button, 0, 2, 1, 1)
        self.layout.addWidget(self.dim_groupbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_sobel_button')
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class CannyMenu(MenuInterface):
    APPLY_BUTTON = 'apply_canny_button'
    widgets = {'sigma': 'sigma_slider',
               'thresholds': 'hysteresis_slider'}
    SIGMAS = {1: 3, 2: 5, 3: 7}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
       
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, RangeSlider):
                        settings['threshold1'] = float(child.low() / 100)
                        settings['threshold2'] = float(child.high() / 100)
                        continue   
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = self.SIGMAS.get(child.value())
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()     
        return settings   
     
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Gaussian Standard Deviation + Labels
        self.gauss_label = QtWidgets.QLabel()
        self.gauss_label.setText('Gaussian Standard Deviation')
        self.gauss_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.gauss_label)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.label1 = QtWidgets.QLabel()
        self.label1.setText('3')
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        
        self.label2 = QtWidgets.QLabel()
        self.label2.setText('5')
        self.label2.setSizePolicy(sizePolicy)
        self.label2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label2, 0, 1, 1, 1)
        
        self.label3 = QtWidgets.QLabel()
        self.label3.setText('7')
        self.label3.setSizePolicy(sizePolicy)
        self.label3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label3, 0, 2, 1, 1)
        self.layout.addLayout(self.gridLayout)
        
        self.gauss_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.gauss_slider.setMinimumHeight(30)
        self.gauss_slider.setMinimum(1)
        self.gauss_slider.setMaximum(3)
        self.gauss_slider.setSliderPosition(1)
        self.gauss_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.gauss_slider.setTickInterval(1)
        self.gauss_slider.setObjectName('sigma_slider')
        self.layout.addWidget(self.gauss_slider)
        
        # Hysteresis Threshold + Label
        self.hysteresis_label = QtWidgets.QLabel()
        self.hysteresis_label.setText('Hysteresis Threshold')
        self.hysteresis_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.hysteresis_label)
        
        self.hysteresis_slider = RangeSlider(QtCore.Qt.Horizontal)
        self.hysteresis_slider.setMinimumHeight(30)
        self.hysteresis_slider.setMinimum(0)
        self.hysteresis_slider.setMaximum(100)
        self.hysteresis_slider.setLow(15)
        self.hysteresis_slider.setHigh(35)
        self.hysteresis_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hysteresis_slider.setTickInterval(10)
        self.hysteresis_slider.setObjectName('hysteresis_slider')
        self.layout.addWidget(self.hysteresis_slider)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_canny_button')
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
       
class SatoMenu(MenuInterface):
    APPLY_BUTTON = 'apply_sato_button'
    widgets = {'sigmas': 'sigma_value_slider',
               'black_ridges': 'black_ridges_checkbox'}

    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = child.value()
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()             
        
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Gaussian Standard Deviation + Labels
        self.sigma_label = QtWidgets.QLabel()
        self.sigma_label.setText('Sigma range')
        self.sigma_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.sigma_label)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        
        
        self.kernel_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.kernel_size_slider.setMinimumHeight(30)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(10)
        self.kernel_size_slider.setSliderPosition(1)
        self.kernel_size_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.kernel_size_slider.setTickInterval(1)
        self.kernel_size_slider.setObjectName('sigma_value_slider')
        self.layout.addWidget(self.kernel_size_slider)
        
        self.black_ridges_checkbox = QtWidgets.QCheckBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.black_ridges_checkbox.sizePolicy().hasHeightForWidth())
        self.black_ridges_checkbox.setSizePolicy(sizePolicy)
        self.black_ridges_checkbox.setObjectName("black_ridges_checkbox")
        self.black_ridges_checkbox.setText("Black ridges")
        self.layout.addWidget(self.black_ridges_checkbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_sato_button')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
        
class MeijeringMenu(MenuInterface):
    APPLY_BUTTON = 'apply_meijering_button'
    widgets = {'sigmas': 'sigma_value_slider',
               'black_ridges': 'black_ridges_checkbox'}

    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = child.value()
                    if isinstance(child, QtWidgets.QCheckBox):
                        settings[key] = child.isChecked()             
        
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # Gaussian Standard Deviation + Labels
        self.sigma_label = QtWidgets.QLabel()
        self.sigma_label.setText('Sigma range')
        self.sigma_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.sigma_label)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        
        
        self.kernel_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.kernel_size_slider.setMinimumHeight(30)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(10)
        self.kernel_size_slider.setSliderPosition(1)
        self.kernel_size_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.kernel_size_slider.setTickInterval(1)
        self.kernel_size_slider.setObjectName('sigma_value_slider')
        self.layout.addWidget(self.kernel_size_slider)
        
        self.black_ridges_checkbox = QtWidgets.QCheckBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.black_ridges_checkbox.sizePolicy().hasHeightForWidth())
        self.black_ridges_checkbox.setSizePolicy(sizePolicy)
        self.black_ridges_checkbox.setObjectName("black_ridges_checkbox")
        self.black_ridges_checkbox.setText("Black ridges")
        self.layout.addWidget(self.black_ridges_checkbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_meijering_button')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class PrewittMenu(MenuInterface):
    APPLY_BUTTON = 'apply_prewitt_button'
    widgets = {'direction': 'dim_groupbox'}
    
    KERNELS = {1: 3, 2: 5, 3: 7}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = self.KERNELS[child.value()]
                    if isinstance(child, QtWidgets.QGroupBox):
                        radio_buttons = [x for x in child.children() if isinstance(x, QtWidgets.QRadioButton)]
                        for radio_button in radio_buttons:
                            if radio_button.isChecked():
                                settings['direction'] = radio_button.text().lower()
                    
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # QRadioButton GroupBox
        self.dim_groupbox = QtWidgets.QGroupBox()
        self.dim_groupbox.setTitle("")
        self.dim_groupbox.setObjectName("dim_groupbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dim_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.combined_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.combined_button.setChecked(True)
        self.combined_button.setText("Combined")
        self.combined_button.setObjectName("combined_button")
        self.gridLayout_3.addWidget(self.combined_button, 0, 0, 1, 1)
        self.vertical_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.vertical_button.setText("Vertical")
        self.vertical_button.setObjectName("vertical_button")
        self.gridLayout_3.addWidget(self.vertical_button, 0, 1, 1, 1)
        self.horizontal_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.horizontal_button.setText("Horizontal")
        self.horizontal_button.setObjectName("horizontal_button")
        self.gridLayout_3.addWidget(self.horizontal_button, 0, 2, 1, 1)
        self.layout.addWidget(self.dim_groupbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_prewitt_button')
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class FaridMenu(MenuInterface):
    APPLY_BUTTON = 'apply_farid_button'
    widgets = {'direction': 'dim_groupbox'}
    
    KERNELS = {1: 3, 2: 5, 3: 7}
    
    def __init__(self):
        super().__init__()
        self.__setupFormatting()
        self.connectEvents()
        self.children = self.children()
    
    def getSettings(self):
        settings = {}
        for key, value in self.widgets.items():
            for child in self.children:
                if child.objectName() == value:
                    if isinstance(child, QtWidgets.QSlider):
                        settings[key] = self.KERNELS[child.value()]
                    if isinstance(child, QtWidgets.QGroupBox):
                        radio_buttons = [x for x in child.children() if isinstance(x, QtWidgets.QRadioButton)]
                        for radio_button in radio_buttons:
                            if radio_button.isChecked():
                                settings['direction'] = radio_button.text().lower()
                    
        return settings
        
    def __setupFormatting(self):
        self.layout = QtWidgets.QVBoxLayout()
        
        # QRadioButton GroupBox
        self.dim_groupbox = QtWidgets.QGroupBox()
        self.dim_groupbox.setTitle("")
        self.dim_groupbox.setObjectName("dim_groupbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dim_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.combined_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.combined_button.setChecked(True)
        self.combined_button.setText("Combined")
        self.combined_button.setObjectName("combined_button")
        self.gridLayout_3.addWidget(self.combined_button, 0, 0, 1, 1)
        self.vertical_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.vertical_button.setText("Vertical")
        self.vertical_button.setObjectName("vertical_button")
        self.gridLayout_3.addWidget(self.vertical_button, 0, 1, 1, 1)
        self.horizontal_button = QtWidgets.QRadioButton(self.dim_groupbox)
        self.horizontal_button.setText("Horizontal")
        self.horizontal_button.setObjectName("horizontal_button")
        self.gridLayout_3.addWidget(self.horizontal_button, 0, 2, 1, 1)
        self.layout.addWidget(self.dim_groupbox)
        
        # Vertical Line
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setLineWidth(0)
        self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_line.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.vertical_line)
        
        # Horizontal Line
        self.horizontal_line = QtWidgets.QFrame()
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(self.horizontal_line)
        
        # Apply Button
        self.button = QtWidgets.QPushButton('Apply changes')
        self.button.setObjectName('apply_farid_button')
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
    