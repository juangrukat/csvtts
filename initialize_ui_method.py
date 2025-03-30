def initialize_ui(self):
    """Initialize UI state"""
    # Populate voice combo box
    self.ui.voiceComboBox.addItems(Settings.VOICES)
    voice_index = self.ui.voiceComboBox.findText(self.settings.default_voice)
    self.ui.voiceComboBox.setCurrentIndex(max(0, voice_index))
    
    # Populate model combo box
    self.ui.modelComboBox.addItems(Settings.MODELS)
    model_index = self.ui.modelComboBox.findText(self.settings.default_model)
    self.ui.modelComboBox.setCurrentIndex(max(0, model_index))
    
    # Set current model label
    self.ui.currentModelLabel.setText(f"{self.settings.default_model}")
    
    # Connect model selection change to update instructions field state
    self.ui.modelComboBox.currentTextChanged.connect(self.update_instructions_field)
    
    # Initialize instructions field state based on current model
    self.update_instructions_field(self.ui.modelComboBox.currentText())
    
    # Disable batch processing by default
    self.toggle_batch_mode(False)
    
    # Disable processing buttons until file is loaded
    self.ui.processButton.setEnabled(False)
    self.ui.batchProcessButton.setEnabled(False)
    self.ui.previewButton.setEnabled(False)
    self.ui.exportButton.setEnabled(False)
    self.ui.stopButton.setEnabled(False)