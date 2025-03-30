# This Python file uses the following encoding: utf-8
import os
import csv
from pathlib import Path

from PySide6.QtCore import QObject, Signal

class CSVProcessor(QObject):
    """Handles CSV file loading and processing"""
    file_loaded = Signal(list, list)  # headers, preview_rows
    error_occurred = Signal(str, str)  # title, message
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.headers = []
        self.rows = []
    
    def load_file(self, file_path):
        """Load a CSV file and extract headers and preview rows"""
        try:
            if not os.path.exists(file_path):
                self.error_occurred.emit("File Not Found", f"The file {file_path} does not exist.")
                return False
            
            if not file_path.lower().endswith('.csv'):
                self.error_occurred.emit("Invalid File", "Please select a CSV file.")
                return False
            
            # Read CSV file
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Get headers
                try:
                    self.headers = next(reader)
                except StopIteration:
                    self.error_occurred.emit("Empty File", "The CSV file is empty.")
                    return False
                
                # Get preview rows (up to 10)
                self.rows = []
                for i, row in enumerate(reader):
                    if i >= 10:  # Limit to 10 rows for preview
                        break
                    self.rows.append(row)
            
            # Store current file
            self.current_file = file_path
            
            # Emit signal with headers and preview rows
            self.file_loaded.emit(self.headers, self.rows)
            
            return True
            
        except Exception as e:
            self.error_occurred.emit("Error Loading File", f"An error occurred: {str(e)}")
            return False
    
    def get_column_data(self, column_index):
        """Get all data from a specific column"""
        if not self.current_file or column_index < 0 or column_index >= len(self.headers):
            return []
        
        column_data = []
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                
                for row in reader:
                    if column_index < len(row):
                        column_data.append(row[column_index])
            
            return column_data
            
        except Exception as e:
            self.error_occurred.emit("Error Reading Column", f"An error occurred: {str(e)}")
            return []
    
    def get_preview_text(self, column_index):
        """Get preview text from a specific column"""
        if column_index < 0 or not self.rows:
            return ""
        
        preview_texts = []
        for row in self.rows:
            if column_index < len(row):
                text = row[column_index].strip()
                if text:  # Skip empty texts
                    preview_texts.append(text)
        
        return "\n\n".join(preview_texts)