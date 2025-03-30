# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.filePath = QLineEdit(self.groupBox)
        self.filePath.setObjectName(u"filePath")

        self.horizontalLayout.addWidget(self.filePath)

        self.browseButton = QPushButton(self.groupBox)
        self.browseButton.setObjectName(u"browseButton")

        self.horizontalLayout.addWidget(self.browseButton)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout = QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.voiceComboBox = QComboBox(self.groupBox_2)
        self.voiceComboBox.setObjectName(u"voiceComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.voiceComboBox)

        self.label_model = QLabel(self.groupBox_2)
        self.label_model.setObjectName(u"label_model")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_model)

        self.modelLayout = QHBoxLayout()
        self.modelLayout.setObjectName(u"modelLayout")
        self.currentModelLabel = QLabel(self.groupBox_2)
        self.currentModelLabel.setObjectName(u"currentModelLabel")

        self.modelLayout.addWidget(self.currentModelLabel)

        self.modelComboBox = QComboBox(self.groupBox_2)
        self.modelComboBox.setObjectName(u"modelComboBox")

        self.modelLayout.addWidget(self.modelComboBox)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.modelLayout)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.instructionsInput = QLineEdit(self.groupBox_2)
        self.instructionsInput.setObjectName(u"instructionsInput")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.instructionsInput)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textPreview = QTextEdit(self.groupBox_3)
        self.textPreview.setObjectName(u"textPreview")

        self.verticalLayout_2.addWidget(self.textPreview)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.batchGroupBox = QGroupBox(self.centralwidget)
        self.batchGroupBox.setObjectName(u"batchGroupBox")
        self.formLayout_2 = QFormLayout(self.batchGroupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.batchGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.columnComboBox = QComboBox(self.batchGroupBox)
        self.columnComboBox.setObjectName(u"columnComboBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.columnComboBox)

        self.label_5 = QLabel(self.batchGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.outputDirPath = QLineEdit(self.batchGroupBox)
        self.outputDirPath.setObjectName(u"outputDirPath")

        self.horizontalLayout_3.addWidget(self.outputDirPath)

        self.outputDirButton = QPushButton(self.batchGroupBox)
        self.outputDirButton.setObjectName(u"outputDirButton")

        self.horizontalLayout_3.addWidget(self.outputDirButton)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.batchCheckBox = QCheckBox(self.batchGroupBox)
        self.batchCheckBox.setObjectName(u"batchCheckBox")

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.batchCheckBox)


        self.verticalLayout.addWidget(self.batchGroupBox)

        self.progressGroupBox = QGroupBox(self.centralwidget)
        self.progressGroupBox.setObjectName(u"progressGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.progressGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.progressBar = QProgressBar(self.progressGroupBox)
        self.progressBar.setObjectName(u"progressBar")

        self.verticalLayout_3.addWidget(self.progressBar)

        self.statusLabel = QLabel(self.progressGroupBox)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.statusLabel)


        self.verticalLayout.addWidget(self.progressGroupBox)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.processButton = QPushButton(self.widget)
        self.processButton.setObjectName(u"processButton")

        self.horizontalLayout_2.addWidget(self.processButton)

        self.batchProcessButton = QPushButton(self.widget)
        self.batchProcessButton.setObjectName(u"batchProcessButton")

        self.horizontalLayout_2.addWidget(self.batchProcessButton)

        self.stopButton = QPushButton(self.widget)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.previewButton = QPushButton(self.widget)
        self.previewButton.setObjectName(u"previewButton")

        self.horizontalLayout_2.addWidget(self.previewButton)

        self.exportButton = QPushButton(self.widget)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout_2.addWidget(self.exportButton)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.actionPreferences = QAction(self.menubar)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuSettings.addAction(self.actionPreferences)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CSV to TTS Converter", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"File Selection", None))
        self.browseButton.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"TTS Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Voice:", None))
        self.label_model.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.currentModelLabel.setText(QCoreApplication.translate("MainWindow", u"tts-1-hd (Default)", None))
        self.currentModelLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-weight: bold;", None))
#if QT_CONFIG(tooltip)
        self.currentModelLabel.setToolTip(QCoreApplication.translate("MainWindow", u"Change default model in Settings", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Instructions:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Text Preview", None))
        self.batchGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Batch Processing", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Text Column:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output Directory:", None))
        self.outputDirPath.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Required - Select output directory", None))
        self.outputDirPath.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"             QGroupBox { padding-top: 15px; margin-top: 10px; }\n"
"             QGroupBox::title { subcontrol-origin: margin; left: 10px; }\n"
"             QPushButton { min-width: 80px; padding: 4px; }\n"
"             QLineEdit:required { border: 1px solid red; }\n"
"            ", None))
        self.outputDirButton.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.batchCheckBox.setText(QCoreApplication.translate("MainWindow", u"Process multiple files in directory", None))
        self.progressGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Ready", None))
        self.processButton.setText(QCoreApplication.translate("MainWindow", u"Process Current File", None))
        self.batchProcessButton.setText(QCoreApplication.translate("MainWindow", u"Process Batch", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.previewButton.setText(QCoreApplication.translate("MainWindow", u"Preview TTS", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export All", None))
#if QT_CONFIG(tooltip)
        self.exportButton.setToolTip(QCoreApplication.translate("MainWindow", u"Export all processed files as a package", None))
#endif // QT_CONFIG(tooltip)
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

