# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

# Import resources
import resources_rc

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.apiTab = QWidget()
        self.apiTab.setObjectName(u"apiTab")
        self.formLayout = QFormLayout(self.apiTab)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.apiTab)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.apiKeyInput = QLineEdit(self.apiTab)
        self.apiKeyInput.setObjectName(u"apiKeyInput")
        self.apiKeyInput.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.apiKeyInput)

        self.label_2 = QLabel(self.apiTab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.endpointInput = QLineEdit(self.apiTab)
        self.endpointInput.setObjectName(u"endpointInput")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.endpointInput)

        self.label_3 = QLabel(self.apiTab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.timeoutInput = QSpinBox(self.apiTab)
        self.timeoutInput.setObjectName(u"timeoutInput")
        self.timeoutInput.setMinimum(1000)
        self.timeoutInput.setMaximum(30000)
        self.timeoutInput.setValue(5000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.timeoutInput)

        self.tabWidget.addTab(self.apiTab, "")
        self.ttsTab = QWidget()
        self.ttsTab.setObjectName(u"ttsTab")
        self.formLayout_2 = QFormLayout(self.ttsTab)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_voice = QLabel(self.ttsTab)
        self.label_voice.setObjectName(u"label_voice")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_voice)

        self.defaultVoiceCombo = QComboBox(self.ttsTab)
        self.defaultVoiceCombo.setObjectName(u"defaultVoiceCombo")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.defaultVoiceCombo)

        self.label_model = QLabel(self.ttsTab)
        self.label_model.setObjectName(u"label_model")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_model)

        self.modelLayout = QHBoxLayout()
        self.modelLayout.setObjectName(u"modelLayout")
        self.modelComboBox = QComboBox(self.ttsTab)
        self.modelComboBox.setObjectName(u"modelComboBox")

        self.modelLayout.addWidget(self.modelComboBox)

        self.refreshModelsButton = QPushButton(self.ttsTab)
        self.refreshModelsButton.setObjectName(u"refreshModelsButton")
        icon = QIcon()
        icon.addFile(u":/icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refreshModelsButton.setIcon(icon)
        self.refreshModelsButton.setFlat(True)

        self.modelLayout.addWidget(self.refreshModelsButton)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.modelLayout)

        self.label_format = QLabel(self.ttsTab)
        self.label_format.setObjectName(u"label_format")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_format)

        self.formatCombo = QComboBox(self.ttsTab)
        self.formatCombo.setObjectName(u"formatCombo")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.formatCombo)

        self.modelInfoGroup = QGroupBox(self.ttsTab)
        self.modelInfoGroup.setObjectName(u"modelInfoGroup")
        self.modelInfoGroup.setFlat(True)
        self.verticalLayout_model = QVBoxLayout(self.modelInfoGroup)
        self.verticalLayout_model.setObjectName(u"verticalLayout_model")
        self.modelDescription = QLabel(self.modelInfoGroup)
        self.modelDescription.setObjectName(u"modelDescription")
        self.modelDescription.setWordWrap(True)

        self.verticalLayout_model.addWidget(self.modelDescription)


        self.formLayout_2.setWidget(3, QFormLayout.SpanningRole, self.modelInfoGroup)

        self.tabWidget.addTab(self.ttsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Application Settings", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"API Key:", None))
        self.label_2.setText(QCoreApplication.translate("SettingsDialog", u"Endpoint:", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"Timeout (ms):", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.apiTab), QCoreApplication.translate("SettingsDialog", u"API Settings", None))
        self.label_voice.setText(QCoreApplication.translate("SettingsDialog", u"Default Voice:", None))
        self.label_model.setText(QCoreApplication.translate("SettingsDialog", u"Default Model:", None))
#if QT_CONFIG(tooltip)
        self.modelComboBox.setToolTip(QCoreApplication.translate("SettingsDialog", u"Select quality/latency tradeoff", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.refreshModelsButton.setToolTip(QCoreApplication.translate("SettingsDialog", u"Refresh available models", None))
#endif // QT_CONFIG(tooltip)
        self.label_format.setText(QCoreApplication.translate("SettingsDialog", u"Output Format:", None))
        self.modelInfoGroup.setTitle(QCoreApplication.translate("SettingsDialog", u"Model Information", None))
        self.modelDescription.setText(QCoreApplication.translate("SettingsDialog", u"\u2022 tts-1: Fast response, standard quality\n"
"\u2022 tts-1-hd: Higher quality, moderate latency\n"
"\u2022 gpt-4o-mini-tts: Advanced features, highest quality", None))
        self.modelDescription.setStyleSheet(QCoreApplication.translate("SettingsDialog", u"font-size: 11px; color: #666; padding: 5px;", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ttsTab), QCoreApplication.translate("SettingsDialog", u"TTS Settings", None))
    # retranslateUi

