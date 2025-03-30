# This Python file uses the following encoding: utf-8
import os
import json
from pathlib import Path

# Import resources
import resources_rc

from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from PySide6.QtCore import QSettings, QStandardPaths

from ui_settings_dialog import Ui_SettingsDialog

class Settings:
    # Available voices and models
    VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 'coral', 'ash', 'ballad', 'sage']
    MODELS = ['tts-1', 'tts-1-hd', 'gpt-4o-mini-tts']
    OUTPUT_FORMATS = ['mp3', 'opus', 'aac', 'flac']
    
    # Default settings
    DEFAULT_ENDPOINT = "https://api.openai.com/v1/audio/speech"
    DEFAULT_TIMEOUT = 10000  # 10 seconds
    DEFAULT_VOICE = "nova"
    DEFAULT_MODEL = "tts-1-hd"
    DEFAULT_FORMAT = "mp3"
    
    def __init__(self):
        # Initialize settings storage
        self.settings = QSettings("CSVtoTTS", "CSVtoTTS")
        
        # Load settings or use defaults
        self.load()
        
        # Create app data directory if it doesn't exist
        self.app_data_dir = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        self.app_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temp directory for previews
        self.temp_dir = self.app_data_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
    
    def load(self):
        """Load settings from storage"""
        self.api_key = self.settings.value("api_key", "")
        self.endpoint = self.settings.value("endpoint", self.DEFAULT_ENDPOINT)
        self.timeout = int(self.settings.value("timeout", self.DEFAULT_TIMEOUT))
        self.default_voice = self.settings.value("default_voice", self.DEFAULT_VOICE)
        self.default_model = self.settings.value("default_model", self.DEFAULT_MODEL)
        self.output_format = self.settings.value("output_format", self.DEFAULT_FORMAT)
    
    def save(self):
        """Save settings to storage"""
        self.settings.setValue("api_key", self.api_key)
        self.settings.setValue("endpoint", self.endpoint)
        self.settings.setValue("timeout", self.timeout)
        self.settings.setValue("default_voice", self.default_voice)
        self.settings.setValue("default_model", self.default_model)
        self.settings.setValue("output_format", self.output_format)
        self.settings.sync()

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        
        self.settings = settings
        
        # Initialize UI with current settings
        self.initialize_ui()
        
        # Connect signals
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self.restore_defaults)
        self.ui.refreshModelsButton.clicked.connect(self.refresh_models)
    
    def initialize_ui(self):
        """Initialize UI with current settings"""
        # API settings
        self.ui.apiKeyInput.setText(self.settings.api_key)
        self.ui.endpointInput.setText(self.settings.endpoint)
        self.ui.timeoutInput.setValue(self.settings.timeout)
        
        # TTS settings
        self.ui.defaultVoiceCombo.addItems(Settings.VOICES)
        voice_index = self.ui.defaultVoiceCombo.findText(self.settings.default_voice)
        self.ui.defaultVoiceCombo.setCurrentIndex(max(0, voice_index))
        
        self.ui.modelComboBox.addItems(Settings.MODELS)
        model_index = self.ui.modelComboBox.findText(self.settings.default_model)
        self.ui.modelComboBox.setCurrentIndex(max(0, model_index))
        
        self.ui.formatCombo.addItems(Settings.OUTPUT_FORMATS)
        format_index = self.ui.formatCombo.findText(self.settings.output_format)
        self.ui.formatCombo.setCurrentIndex(max(0, format_index))
    
    def accept(self):
        """Save settings and close dialog"""
        # Validate API key
        api_key = self.ui.apiKeyInput.text().strip()
        if not api_key:
            QMessageBox.warning(self, "API Key Required", "Please enter your OpenAI API key.")
            return
        
        # Save settings
        self.settings.api_key = api_key
        self.settings.endpoint = self.ui.endpointInput.text().strip()
        self.settings.timeout = self.ui.timeoutInput.value()
        self.settings.default_voice = self.ui.defaultVoiceCombo.currentText()
        self.settings.default_model = self.ui.modelComboBox.currentText()
        self.settings.output_format = self.ui.formatCombo.currentText()
        
        self.settings.save()
        
        super().accept()
    
    def restore_defaults(self):
        """Restore default settings"""
        self.ui.endpointInput.setText(Settings.DEFAULT_ENDPOINT)
        self.ui.timeoutInput.setValue(Settings.DEFAULT_TIMEOUT)
        
        voice_index = self.ui.defaultVoiceCombo.findText(Settings.DEFAULT_VOICE)
        self.ui.defaultVoiceCombo.setCurrentIndex(max(0, voice_index))
        
        model_index = self.ui.modelComboBox.findText(Settings.DEFAULT_MODEL)
        self.ui.modelComboBox.setCurrentIndex(max(0, model_index))
        
        format_index = self.ui.formatCombo.findText(Settings.DEFAULT_FORMAT)
        self.ui.formatCombo.setCurrentIndex(max(0, format_index))
    
    def refresh_models(self):
        """Refresh available models from OpenAI API"""
        # In a real implementation, this would query the OpenAI API
        # for available models. For now, we'll just show a message.
        QMessageBox.information(
            self,
            "Models Refreshed",
            "Using built-in model list. In a production app, this would query the OpenAI API."
        )