# This Python file uses the following encoding: utf-8
import sys
import os
import csv
import time
import platform
from pathlib import Path

# Import resources
import resources_rc

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QMenu, QInputDialog, QPushButton, QFormLayout
)
from PySide6.QtCore import Qt, QDir, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QAction

# Import UI
from ui_form import Ui_MainWindow

# Import custom modules
from settings import Settings, SettingsDialog
from tts_processor import TTSProcessor, TTSWorker
from csv_processor import CSVProcessor

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize settings
        self.settings = Settings()
        
        # Initialize processors
        self.csv_processor = CSVProcessor()
        self.tts_processor = TTSProcessor(self.settings)
        
        # Current worker thread
        self.current_worker = None
        
        # Track processed files
        self.processed_files = []
        
        # Store batch files
        self.batch_files = []
        
        # Connect signals
        self.ui.browseButton.clicked.connect(self.browse_file)
        self.ui.outputDirButton.clicked.connect(self.browse_output_dir)
        self.ui.batchCheckBox.toggled.connect(self.toggle_batch_mode)
        self.ui.processButton.clicked.connect(self.process_current_file)
        self.ui.batchProcessButton.clicked.connect(self.process_batch)
        self.ui.stopButton.clicked.connect(self.stop_processing)
        self.ui.previewButton.clicked.connect(self.preview_tts)
        self.ui.exportButton.clicked.connect(self.export_all)
        self.ui.actionPreferences.triggered.connect(self.show_settings)
        
        # CSV processor signals
        self.csv_processor.file_loaded.connect(self.on_csv_loaded)
        self.csv_processor.error_occurred.connect(self.show_error)
        
        # TTS processor signals
        self.tts_processor.progress_updated.connect(self.update_progress)
        self.tts_processor.processing_complete.connect(self.on_processing_complete)
        self.tts_processor.processing_error.connect(self.show_error)
        self.tts_processor.preview_ready.connect(self.play_preview)
        
        # Set up menu
        self.ui.menuFile.addAction("Open CSV...", self.browse_file)
        self.ui.menuFile.addSeparator()
        self.ui.menuFile.addAction("Exit", self.close)
        self.ui.menuHelp.addAction("About", self.show_about)
        self.ui.menuSettings.addAction(self.ui.actionPreferences)
        
        # Initialize UI state - call this after connecting signals
        self.initialize_ui()
    
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
        
        # Make sure batch checkbox is always enabled
        self.ui.batchCheckBox.setEnabled(True)
        
        # Disable batch processing by default
        self.toggle_batch_mode(False)
        
        # Disable processing buttons until file is loaded
        self.ui.processButton.setEnabled(False)
        self.ui.batchProcessButton.setEnabled(False)
        self.ui.previewButton.setEnabled(False)
        self.ui.exportButton.setEnabled(False)
        self.ui.stopButton.setEnabled(False)
    
    def browse_file(self):
        """Open file dialog to select CSV files"""
        if self.ui.batchCheckBox.isChecked():
            # Allow selecting multiple files in batch mode
            file_paths, _ = QFileDialog.getOpenFileNames(
                self,
                "Select CSV Files",
                QDir.homePath(),
                "CSV Files (*.csv);;All Files (*.*)"
            )
            
            if file_paths:
                # Store all selected files for batch processing
                self.batch_files = file_paths
                # Display the first file in the UI
                self.ui.filePath.setText(file_paths[0])
                self.load_csv_file(file_paths[0])
                # Update status to show number of files selected
                self.ui.statusLabel.setText(f"{len(file_paths)} files selected for batch processing")
                # Enable batch process button if we have an output directory
                if self.ui.outputDirPath.text():
                    self.ui.batchProcessButton.setEnabled(True)
        else:
            # Single file selection mode
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select CSV File",
                QDir.homePath(),
                "CSV Files (*.csv);;All Files (*.*)"
            )
            
            if file_path:
                self.ui.filePath.setText(file_path)
                self.load_csv_file(file_path)
    
    def load_csv_file(self, file_path):
        """Load a CSV file and update UI"""
        if self.csv_processor.load_file(file_path):
            # Enable processing buttons
            self.ui.processButton.setEnabled(True)
            self.ui.previewButton.setEnabled(True)
    
    def on_csv_loaded(self, headers, preview_rows):
        """Handle CSV file loaded event"""
        # Populate column combo box
        self.ui.columnComboBox.clear()
        self.ui.columnComboBox.addItems(headers)
        
        # Connect column selection change to update preview
        self.ui.columnComboBox.currentIndexChanged.connect(self.update_preview_text)
        
        # Show preview in text area
        if preview_rows and len(preview_rows) > 0:
            selected_column = self.ui.columnComboBox.currentIndex()
            if selected_column >= 0 and selected_column < len(headers):
                self.update_preview_text(selected_column)
    
    def browse_output_dir(self):
        """Open directory dialog to select output directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            QDir.homePath(),
            QFileDialog.ShowDirsOnly
        )
        
        if dir_path:
            self.ui.outputDirPath.setText(dir_path)
            # Enable batch processing if we have a file and output directory
            self.ui.batchProcessButton.setEnabled(
                bool(self.ui.filePath.text()) and bool(dir_path)
            )
    
    def toggle_batch_mode(self, enabled):
        """Toggle batch processing mode"""
        # Keep the batch checkbox always enabled, but enable/disable the controls inside the batch group
        # Find all widgets in the batch group except the checkbox
        from PySide6.QtWidgets import QFormLayout
        
        # Enable batch processing UI elements
        self.ui.batchGroupBox.setEnabled(True)  # Always keep the group box enabled
        
        # Update button states
        if enabled and self.ui.filePath.text() and self.ui.outputDirPath.text():
            self.ui.batchProcessButton.setEnabled(True)
        else:
            self.ui.batchProcessButton.setEnabled(False)
            
        # Clear batch files when disabling batch mode
        if not enabled:
            self.batch_files = []
        
        # Update browse button tooltip and behavior based on mode
        if enabled:
            self.ui.browseButton.setToolTip("Select multiple CSV files")
            # Make sure the batch checkbox is checked (in case this was called programmatically)
            self.ui.batchCheckBox.setChecked(True)
        else:
            self.ui.browseButton.setToolTip("Select a CSV file")
            
        # Add folder selection button for batch mode
        if not hasattr(self, 'folderSelectButton'):
            self.folderSelectButton = QPushButton("Select Folder", self.ui.batchGroupBox)
            self.folderSelectButton.setToolTip("Select a folder containing CSV files")
            self.ui.formLayout_2.addRow("Select Folder:", self.folderSelectButton)
            self.folderSelectButton.clicked.connect(self.browse_folder)
            
        self.folderSelectButton.setVisible(enabled)
    
    def process_current_file(self):
        """Process the current CSV file"""
        if not self.ui.filePath.text():
            self.show_error("No file selected", "Please select a CSV file first.")
            return
            
        if not self.ui.outputDirPath.text():
            self.browse_output_dir()
            if not self.ui.outputDirPath.text():
                return
        
        # Get selected column
        column_index = self.ui.columnComboBox.currentIndex()
        if column_index < 0:
            self.show_error("No column selected", "Please select a text column to process.")
            return
        
        # Get TTS settings
        voice = self.ui.voiceComboBox.currentText()
        model = self.ui.modelComboBox.currentText() or self.settings.default_model
        instructions = self.ui.instructionsInput.text()
        
        # Start processing
        self.start_processing([
            {
                'file_path': self.ui.filePath.text(),
                'column_index': column_index,
                'voice': voice,
                'model': model,
                'instructions': instructions,
                'output_dir': self.ui.outputDirPath.text()
            }
        ])
    
    def update_preview_text(self, column_index):
        """Update preview text based on selected column"""
        if not self.csv_processor.rows:
            return
            
        preview_text = "\n\n".join([row[column_index] if column_index < len(row) else "" 
                              for row in self.csv_processor.rows])
        self.ui.textPreview.setText(preview_text)
    
    def process_batch(self):
        """Process multiple CSV files in batch mode"""
        if not self.ui.outputDirPath.text():
            self.browse_output_dir()
            if not self.ui.outputDirPath.text():
                return
        
        # Get selected column
        column_index = self.ui.columnComboBox.currentIndex()
        if column_index < 0:
            self.show_error("No column selected", "Please select a text column to process.")
            return
        
        # Get TTS settings
        voice = self.ui.voiceComboBox.currentText()
        model = self.ui.modelComboBox.currentText() or self.settings.default_model
        instructions = self.ui.instructionsInput.text()
        
        # If batch checkbox is checked, process selected files
        if self.ui.batchCheckBox.isChecked():
            files_to_process = []
            
            # If we have batch files selected, use those
            if self.batch_files:
                for file_path in self.batch_files:
                    files_to_process.append({
                        'file_path': file_path,
                        'column_index': column_index,
                        'voice': voice,
                        'model': model,
                        'instructions': instructions,
                        'output_dir': self.ui.outputDirPath.text()
                    })
            else:
                # Fallback to processing all CSV files in the directory of the current file
                current_file = self.ui.filePath.text()
                if not current_file:
                    self.show_error("No file selected", "Please select a CSV file first.")
                    return
                    
                directory = os.path.dirname(current_file)
                
                # Find all CSV files in the directory
                for file_name in os.listdir(directory):
                    if file_name.lower().endswith('.csv'):
                        file_path = os.path.join(directory, file_name)
                        files_to_process.append({
                            'file_path': file_path,
                            'column_index': column_index,
                            'voice': voice,
                            'model': model,
                            'instructions': instructions,
                            'output_dir': self.ui.outputDirPath.text()
                        })
            
            if not files_to_process:
                self.show_error("No CSV files found", "No CSV files found to process")
                return
                
            # Start processing
            self.start_processing(files_to_process)
        else:
            # Just process the current file
            self.process_current_file()
    
    def start_processing(self, files_to_process):
        """Start processing files"""
        # Update UI
        self.ui.processButton.setEnabled(False)
        self.ui.batchProcessButton.setEnabled(False)
        self.ui.previewButton.setEnabled(False)
        self.ui.exportButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        
        # Reset progress
        self.ui.progressBar.setValue(0)
        self.ui.statusLabel.setText("Processing...")
        
        # Start worker
        self.current_worker = self.tts_processor.process_files(files_to_process)
    
    def stop_processing(self):
        """Stop current processing"""
        if self.current_worker and self.current_worker.isRunning():
            self.tts_processor.stop_processing()
            self.ui.statusLabel.setText("Stopping...")
    
    def update_progress(self, current, total, message):
        """Update progress bar and status"""
        progress = int((current / total) * 100) if total > 0 else 0
        self.ui.progressBar.setValue(progress)
        self.ui.statusLabel.setText(message)
    
    def on_processing_complete(self, processed_files):
        """Handle processing complete event"""
        # Update UI
        self.ui.processButton.setEnabled(True)
        self.ui.batchProcessButton.setEnabled(self.ui.batchCheckBox.isChecked() and bool(self.ui.outputDirPath.text()))
        self.ui.previewButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.exportButton.setEnabled(len(processed_files) > 0)
        
        # Update status
        self.ui.progressBar.setValue(100)
        self.ui.statusLabel.setText(f"Completed: {len(processed_files)} files processed")
        
        # Store processed files
        self.processed_files = processed_files
        print(f"DEBUG: Stored {len(processed_files)} processed files. Export button enabled: {len(processed_files) > 0}")
        if len(processed_files) > 0:
            # Log the first file for debugging
            print(f"DEBUG: First processed file: {processed_files[0].get('output_file', 'No output file')}")
        
        # Show completion message
        QMessageBox.information(
            self,
            "Processing Complete",
            f"Successfully processed {len(processed_files)} files. You can now use 'Export All' to save these files to a directory of your choice."
        )
    
    def preview_tts(self):
        """Generate and play a TTS preview"""
        # Get selected text
        text = self.ui.textPreview.toPlainText()
        if not text:
            self.show_error("No text to preview", "Please select a file with text content first.")
            return
        
        # If text is too long, ask for confirmation
        if len(text) > 500:
            response = QMessageBox.question(
                self,
                "Long Text",
                "The selected text is quite long. Would you like to preview only the first 500 characters?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if response == QMessageBox.Yes:
                text = text[:500]
            
        # Get TTS settings
        voice = self.ui.voiceComboBox.currentText()
        model = self.ui.modelComboBox.currentText() or self.settings.default_model
        instructions = self.ui.instructionsInput.text()
        
        # Update UI
        self.ui.previewButton.setEnabled(False)
        self.ui.statusLabel.setText("Generating preview...")
        
        # Generate preview
        self.tts_processor.generate_preview(text, voice, model, instructions)
    
    def play_preview(self, preview_file):
        """Play the generated preview"""
        # Update UI
        self.ui.previewButton.setEnabled(True)
        self.ui.statusLabel.setText("Ready")
        
        # Open the file with the default audio player
        QDesktopServices.openUrl(QUrl.fromLocalFile(preview_file))
    
    def export_all(self):
        """Export all processed files as a package"""
        print(f"DEBUG: Export all called. Processed files count: {len(self.processed_files)}")
        if not self.processed_files:
            self.show_error("No files to export", "No files have been processed yet. Please process at least one file before exporting.")
            self.ui.statusLabel.setText("Error: No files to export")
            return
        
        # Ask for export directory
        export_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Export Directory",
            QDir.homePath(),
            QFileDialog.ShowDirsOnly
        )
        
        if not export_dir:
            return
        
        # Copy all processed files to export directory
        try:
            import shutil
            count = 0
            
            for file_info in self.processed_files:
                output_file = file_info.get('output_file')
                if output_file and os.path.exists(output_file):
                    file_name = os.path.basename(output_file)
                    dest_path = os.path.join(export_dir, file_name)
                    shutil.copy2(output_file, dest_path)
                    count += 1
            
            # Show success message
            QMessageBox.information(
                self,
                "Export Complete",
                f"Successfully exported {count} files to {export_dir}"
            )
            
            # Open the export directory
            QDesktopServices.openUrl(QUrl.fromLocalFile(export_dir))
            
        except Exception as e:
            self.show_error("Export Error", f"Error exporting files: {str(e)}")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            # Reload settings
            self.settings.load()
            
            # Update UI
            voice_index = self.ui.voiceComboBox.findText(self.settings.default_voice)
            self.ui.voiceComboBox.setCurrentIndex(max(0, voice_index))
            
            model_index = self.ui.modelComboBox.findText(self.settings.default_model)
            self.ui.modelComboBox.setCurrentIndex(max(0, model_index))
            
            self.ui.currentModelLabel.setText(f"{self.settings.default_model}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About CSV to TTS Converter",
            "<h3>CSV to TTS Converter</h3>"
            "<p>A tool for converting CSV text to speech using OpenAI's TTS API.</p>"
            "<p>Version 1.0</p>"
        )
    
    def show_error(self, title, message):
        """Show error message"""
        QMessageBox.critical(self, title, message)
    
    def update_instructions_field(self, model):
        """Enable or disable instructions field based on model"""
        # Only enable instructions for gpt-4o-mini-tts model
        instructions_enabled = model == "gpt-4o-mini-tts"
        self.ui.instructionsInput.setEnabled(instructions_enabled)
        
        # Set placeholder text to guide users
        if instructions_enabled:
            self.ui.instructionsInput.setPlaceholderText("Enter instructions for voice style (accent, emotion, etc.)")
        else:
            self.ui.instructionsInput.setPlaceholderText("Instructions only available with gpt-4o-mini-tts model")
            # Clear any existing instructions when switching to a model that doesn't support it
            self.ui.instructionsInput.clear()
    
    def browse_folder(self):
        """Open directory dialog to select a folder containing CSV files"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder with CSV Files",
            QDir.homePath(),
            QFileDialog.ShowDirsOnly
        )
        
        if folder_path:
            # Find all CSV files in the selected folder
            self.batch_files = []
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    self.batch_files.append(file_path)
            
            if self.batch_files:
                # Display the first file in the UI
                self.ui.filePath.setText(self.batch_files[0])
                self.load_csv_file(self.batch_files[0])
                # Update status to show number of files found
                self.ui.statusLabel.setText(f"Found {len(self.batch_files)} CSV files in folder")
                # Enable batch processing button
                if self.ui.outputDirPath.text():
                    self.ui.batchProcessButton.setEnabled(True)
            else:
                self.show_error("No CSV Files", f"No CSV files found in {folder_path}")
                self.ui.statusLabel.setText("No CSV files found in selected folder")
                self.ui.batchProcessButton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
