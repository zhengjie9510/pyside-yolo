# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpinBox, QStatusBar, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(840, 500)
        icon = QIcon()
        icon.addFile(u"icons/window.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(200, 0))
        self.widget.setMaximumSize(QSize(250, 16777215))
        self.widget.setSizeIncrement(QSize(0, 0))
        self.widget.setBaseSize(QSize(0, 0))
        self.widget.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.widget_setting = QWidget(self.widget)
        self.widget_setting.setObjectName(u"widget_setting")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_setting.sizePolicy().hasHeightForWidth())
        self.widget_setting.setSizePolicy(sizePolicy1)
        self.widget_setting.setBaseSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget_setting)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_setting = QFormLayout()
        self.formLayout_setting.setObjectName(u"formLayout_setting")
        self.formLayout_setting.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_setting.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout_setting.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout_setting.setHorizontalSpacing(5)
        self.formLayout_setting.setVerticalSpacing(10)
        self.formLayout_setting.setContentsMargins(-1, 0, -1, -1)
        self.label_model = QLabel(self.widget_setting)
        self.label_model.setObjectName(u"label_model")
        sizePolicy.setHeightForWidth(self.label_model.sizePolicy().hasHeightForWidth())
        self.label_model.setSizePolicy(sizePolicy)
        self.label_model.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.label_model.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_setting.setWidget(1, QFormLayout.LabelRole, self.label_model)

        self.horizontalLayout_model = QHBoxLayout()
        self.horizontalLayout_model.setObjectName(u"horizontalLayout_model")
        self.lineEdit_model = QLineEdit(self.widget_setting)
        self.lineEdit_model.setObjectName(u"lineEdit_model")
        self.lineEdit_model.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_model.setInputMethodHints(Qt.ImhNone)
        self.lineEdit_model.setFrame(True)

        self.horizontalLayout_model.addWidget(self.lineEdit_model)

        self.button_model = QPushButton(self.widget_setting)
        self.button_model.setObjectName(u"button_model")
        self.button_model.setEnabled(True)
        self.button_model.setMaximumSize(QSize(30, 16777215))
        icon1 = QIcon()
        icon1.addFile(u"icons/file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_model.setIcon(icon1)
        self.button_model.setIconSize(QSize(20, 20))
        self.button_model.setFlat(True)

        self.horizontalLayout_model.addWidget(self.button_model)


        self.formLayout_setting.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_model)

        self.label_task = QLabel(self.widget_setting)
        self.label_task.setObjectName(u"label_task")
        sizePolicy.setHeightForWidth(self.label_task.sizePolicy().hasHeightForWidth())
        self.label_task.setSizePolicy(sizePolicy)
        self.label_task.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.formLayout_setting.setWidget(2, QFormLayout.LabelRole, self.label_task)

        self.horizontalLayout_task = QHBoxLayout()
        self.horizontalLayout_task.setObjectName(u"horizontalLayout_task")
        self.radioButton_detect = QRadioButton(self.widget_setting)
        self.radioButton_detect.setObjectName(u"radioButton_detect")
        sizePolicy.setHeightForWidth(self.radioButton_detect.sizePolicy().hasHeightForWidth())
        self.radioButton_detect.setSizePolicy(sizePolicy)
        self.radioButton_detect.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.radioButton_detect.setChecked(True)

        self.horizontalLayout_task.addWidget(self.radioButton_detect)

        self.radioButton_track = QRadioButton(self.widget_setting)
        self.radioButton_track.setObjectName(u"radioButton_track")
        sizePolicy.setHeightForWidth(self.radioButton_track.sizePolicy().hasHeightForWidth())
        self.radioButton_track.setSizePolicy(sizePolicy)
        self.radioButton_track.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.horizontalLayout_task.addWidget(self.radioButton_track)


        self.formLayout_setting.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_task)

        self.label_input = QLabel(self.widget_setting)
        self.label_input.setObjectName(u"label_input")
        sizePolicy.setHeightForWidth(self.label_input.sizePolicy().hasHeightForWidth())
        self.label_input.setSizePolicy(sizePolicy)
        self.label_input.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.formLayout_setting.setWidget(3, QFormLayout.LabelRole, self.label_input)

        self.horizontalLayout_input = QHBoxLayout()
        self.horizontalLayout_input.setObjectName(u"horizontalLayout_input")
        self.button_file = QPushButton(self.widget_setting)
        self.button_file.setObjectName(u"button_file")
        self.button_file.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.button_file.setAcceptDrops(False)
        self.button_file.setAutoFillBackground(False)
        self.button_file.setInputMethodHints(Qt.ImhNone)
        self.button_file.setIcon(icon1)
        self.button_file.setIconSize(QSize(20, 20))
        self.button_file.setAutoExclusive(False)
        self.button_file.setAutoRepeatDelay(300)
        self.button_file.setAutoDefault(False)
        self.button_file.setFlat(True)

        self.horizontalLayout_input.addWidget(self.button_file)

        self.button_local_camera = QPushButton(self.widget_setting)
        self.button_local_camera.setObjectName(u"button_local_camera")
        self.button_local_camera.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon2 = QIcon()
        icon2.addFile(u"icons/camera.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_local_camera.setIcon(icon2)
        self.button_local_camera.setIconSize(QSize(20, 20))
        self.button_local_camera.setFlat(True)

        self.horizontalLayout_input.addWidget(self.button_local_camera)

        self.button_network_camera = QPushButton(self.widget_setting)
        self.button_network_camera.setObjectName(u"button_network_camera")
        self.button_network_camera.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon3 = QIcon()
        icon3.addFile(u"icons/network.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_network_camera.setIcon(icon3)
        self.button_network_camera.setIconSize(QSize(20, 20))
        self.button_network_camera.setFlat(True)

        self.horizontalLayout_input.addWidget(self.button_network_camera)


        self.formLayout_setting.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_input)

        self.label_conf = QLabel(self.widget_setting)
        self.label_conf.setObjectName(u"label_conf")
        sizePolicy.setHeightForWidth(self.label_conf.sizePolicy().hasHeightForWidth())
        self.label_conf.setSizePolicy(sizePolicy)
        self.label_conf.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.formLayout_setting.setWidget(4, QFormLayout.LabelRole, self.label_conf)

        self.spinBox_conf = QSpinBox(self.widget_setting)
        self.spinBox_conf.setObjectName(u"spinBox_conf")
        font = QFont()
        font.setPointSize(10)
        self.spinBox_conf.setFont(font)
        self.spinBox_conf.setAcceptDrops(False)
        self.spinBox_conf.setWrapping(False)
        self.spinBox_conf.setAccelerated(False)
        self.spinBox_conf.setKeyboardTracking(True)
        self.spinBox_conf.setMaximum(100)
        self.spinBox_conf.setValue(25)

        self.formLayout_setting.setWidget(5, QFormLayout.LabelRole, self.spinBox_conf)

        self.horizontalSlider_conf = QSlider(self.widget_setting)
        self.horizontalSlider_conf.setObjectName(u"horizontalSlider_conf")
        self.horizontalSlider_conf.setMaximum(100)
        self.horizontalSlider_conf.setSliderPosition(25)
        self.horizontalSlider_conf.setOrientation(Qt.Horizontal)

        self.formLayout_setting.setWidget(5, QFormLayout.FieldRole, self.horizontalSlider_conf)

        self.label_iou = QLabel(self.widget_setting)
        self.label_iou.setObjectName(u"label_iou")
        sizePolicy.setHeightForWidth(self.label_iou.sizePolicy().hasHeightForWidth())
        self.label_iou.setSizePolicy(sizePolicy)
        self.label_iou.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.formLayout_setting.setWidget(6, QFormLayout.LabelRole, self.label_iou)

        self.spinBox_iou = QSpinBox(self.widget_setting)
        self.spinBox_iou.setObjectName(u"spinBox_iou")
        self.spinBox_iou.setFont(font)
        self.spinBox_iou.setMaximum(100)
        self.spinBox_iou.setValue(70)

        self.formLayout_setting.setWidget(7, QFormLayout.LabelRole, self.spinBox_iou)

        self.horizontalSlider_iou = QSlider(self.widget_setting)
        self.horizontalSlider_iou.setObjectName(u"horizontalSlider_iou")
        self.horizontalSlider_iou.setMaximum(100)
        self.horizontalSlider_iou.setSliderPosition(70)
        self.horizontalSlider_iou.setOrientation(Qt.Horizontal)

        self.formLayout_setting.setWidget(7, QFormLayout.FieldRole, self.horizontalSlider_iou)

        self.label_size = QLabel(self.widget_setting)
        self.label_size.setObjectName(u"label_size")

        self.formLayout_setting.setWidget(8, QFormLayout.LabelRole, self.label_size)

        self.spinBox_size = QSpinBox(self.widget_setting)
        self.spinBox_size.setObjectName(u"spinBox_size")
        self.spinBox_size.setFont(font)
        self.spinBox_size.setInputMethodHints(Qt.ImhDigitsOnly)
        self.spinBox_size.setMinimum(640)
        self.spinBox_size.setMaximum(1280)
        self.spinBox_size.setSingleStep(32)
        self.spinBox_size.setValue(640)

        self.formLayout_setting.setWidget(9, QFormLayout.LabelRole, self.spinBox_size)

        self.horizontalSlider_size = QSlider(self.widget_setting)
        self.horizontalSlider_size.setObjectName(u"horizontalSlider_size")
        self.horizontalSlider_size.setMinimum(640)
        self.horizontalSlider_size.setMaximum(1280)
        self.horizontalSlider_size.setSingleStep(32)
        self.horizontalSlider_size.setTracking(True)
        self.horizontalSlider_size.setOrientation(Qt.Horizontal)

        self.formLayout_setting.setWidget(9, QFormLayout.FieldRole, self.horizontalSlider_size)


        self.verticalLayout_2.addLayout(self.formLayout_setting)


        self.verticalLayout.addWidget(self.widget_setting)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.horizontalLayout.addWidget(self.widget)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label_image = QLabel(self.centralwidget)
        self.label_image.setObjectName(u"label_image")
        sizePolicy.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy)
        self.label_image.setMinimumSize(QSize(300, 200))
        self.label_image.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_image)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 840, 36))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.radioButton_detect, self.button_local_camera)
        QWidget.setTabOrder(self.button_local_camera, self.lineEdit_model)
        QWidget.setTabOrder(self.lineEdit_model, self.button_file)
        QWidget.setTabOrder(self.button_file, self.textBrowser)
        QWidget.setTabOrder(self.textBrowser, self.button_network_camera)
        QWidget.setTabOrder(self.button_network_camera, self.button_model)
        QWidget.setTabOrder(self.button_model, self.radioButton_track)

        self.retranslateUi(MainWindow)
        self.horizontalSlider_conf.valueChanged.connect(self.spinBox_conf.setValue)
        self.horizontalSlider_iou.valueChanged.connect(self.spinBox_iou.setValue)
        self.spinBox_iou.valueChanged.connect(self.horizontalSlider_iou.setValue)
        self.spinBox_conf.valueChanged.connect(self.horizontalSlider_conf.setValue)
        self.spinBox_size.valueChanged.connect(self.horizontalSlider_size.setValue)
        self.horizontalSlider_size.valueChanged.connect(self.spinBox_size.setValue)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PySide-YOLO", None))
        self.label_model.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.lineEdit_model.setText("")
        self.button_model.setText("")
        self.label_task.setText(QCoreApplication.translate("MainWindow", u"Task:", None))
        self.radioButton_detect.setText(QCoreApplication.translate("MainWindow", u"Detect", None))
        self.radioButton_track.setText(QCoreApplication.translate("MainWindow", u"Track", None))
        self.label_input.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.button_file.setText("")
        self.button_local_camera.setText("")
        self.button_network_camera.setText("")
        self.label_conf.setText(QCoreApplication.translate("MainWindow", u"conf:", None))
        self.label_iou.setText(QCoreApplication.translate("MainWindow", u"IoU:", None))
        self.label_size.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.label_image.setText("")
    # retranslateUi

