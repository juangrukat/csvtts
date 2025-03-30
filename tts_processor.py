# This Python file uses the following encoding: utf-8
import os
import time
import tempfile
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, QMutex, QWaitCondition

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class TTSWorker(QThread):
    """Worker thread for TTS processing"""
    progress_updated = Signal(int, int, str)  # current, total, message
    processing_complete = Signal(list)  # list of processed files
    processing_error = Signal(str, str)  # title, message
    
    def __init__(self, settings, files_to_process):
        super().__init__()
        self.settings = settings
        self.files_to_process = files_to_process
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.abort = False
    
    def run(self):
        """Process files in a separate thread"""
        processed_files = []
        
        if not OPENAI_AVAILABLE:
            self.processing_error.emit(
                "OpenAI API Not Available",
                "The OpenAI package is not installed. Please install it with 'pip install openai'."
            )
            return
        
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=self.settings.api_key)
            
            total_files = len(self.files_to_process)
            for i, file_info in enumerate(self.files_to_process):
                # Check if processing should be aborted
                self.mutex.lock()
                if self.abort:
                    self.mutex.unlock()
                    break
                self.mutex.unlock()
                
                try:
                    # Extract file info
                    file_path = file_info['file_path']
                    column_index = file_info['column_index']
                    voice = file_info['voice']
                    model = file_info['model']
                    instructions = file_info['instructions']
                    output_dir = file_info['output_dir']
                    
                    # Update progress
                    file_name = os.path.basename(file_path)
                    self.progress_updated.emit(
                        i, total_files,
                        f"Processing {file_name} ({i+1}/{total_files})"
                    )
                    
                    # Read CSV file
                    import csv
                    texts = []
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)  # Skip header row
                        
                        for row in reader:
                            if column_index < len(row):
                                text = row[column_index].strip()
                                if text:  # Skip empty texts
                                    texts.append(text)
                    
                    # Process each text entry
                    for j, text in enumerate(texts):
                        # Check if processing should be aborted
                        self.mutex.lock()
                        if self.abort:
                            self.mutex.unlock()
                            break
                        self.mutex.unlock()
                        
                        # Update progress
                        self.progress_updated.emit(
                            i + (j / len(texts)), total_files,
                            f"Processing {file_name}: {j+1}/{len(texts)}"
                        )
                        
                        # Generate output file name
                        base_name = os.path.splitext(file_name)[0]
                        output_file = os.path.join(
                            output_dir,
                            f"{base_name}_{j+1}.{self.settings.output_format}"
                        )
                        
                        # Generate speech
                        try:
                            # Create parameters for the API call
                            params = {
                                "model": model,
                                "voice": voice,
                                "input": text,
                                "response_format": self.settings.output_format
                            }
                            
                            # Only add instructions parameter for models that support it
                            # and only if instructions are provided
                            if model == "gpt-4o-mini-tts" and instructions:
                                try:
                                    # Try with instructions parameter
                                    with client.audio.speech.with_streaming_response.create(
                                        **params,
                                        instructions=instructions
                                    ) as response:
                                        response.stream_to_file(output_file)
                                except Exception as e:
                                    if "unexpected keyword argument 'instructions'" in str(e):
                                        # Fall back to without instructions if not supported
                                        response = client.audio.speech.create(**params)
                                        response.stream_to_file(output_file)
                                    else:
                                        raise
                            else:
                                # For older models or when no instructions are provided
                                response = client.audio.speech.create(**params)
                                response.stream_to_file(output_file)
                        except Exception as e:
                            # Handle specific API errors
                            error_msg = str(e)
                            if "unexpected keyword argument 'instructions'" in error_msg:
                                self.processing_error.emit(
                                    "API Error",
                                    f"There was an error using instructions with the model '{model}'. This might be due to an API version mismatch or the OpenAI client library not supporting this feature yet."
                                )
                            else:
                                # Re-raise other exceptions
                                raise
                        
                        # Add to processed files
                        processed_files.append({
                            'input_file': file_path,
                            'output_file': output_file,
                            'text': text,
                            'voice': voice,
                            'model': model
                        })
                        
                        # Small delay to prevent API rate limiting
                        time.sleep(0.5)
                    
                except Exception as e:
                    self.processing_error.emit(
                        "Processing Error",
                        f"Error processing {file_path}: {str(e)}"
                    )
            
            # Signal completion
            self.progress_updated.emit(total_files, total_files, "Processing complete")
            self.processing_complete.emit(processed_files)
            
        except Exception as e:
            self.processing_error.emit("Error", f"An error occurred: {str(e)}")
    
    def stop(self):
        """Stop processing"""
        self.mutex.lock()
        self.abort = True
        self.mutex.unlock()
        self.condition.wakeAll()

class TTSProcessor(QObject):
    """Handles TTS processing using OpenAI API"""
    progress_updated = Signal(int, int, str)  # current, total, message
    processing_complete = Signal(list)  # list of processed files
    processing_error = Signal(str, str)  # title, message
    preview_ready = Signal(str)  # preview file path
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.current_worker = None
    
    def process_files(self, files_to_process):
        """Process files using a worker thread"""
        # Stop any existing worker
        self.stop_processing()
        
        # Create and start new worker
        self.current_worker = TTSWorker(self.settings, files_to_process)
        self.current_worker.progress_updated.connect(self.progress_updated)
        self.current_worker.processing_complete.connect(self.processing_complete)
        self.current_worker.processing_error.connect(self.processing_error)
        self.current_worker.start()
        
        return self.current_worker
    
    def stop_processing(self):
        """Stop current processing"""
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            self.current_worker.wait()
    
    def generate_preview(self, text, voice, model, instructions):
        """Generate a preview of the TTS"""
        if not OPENAI_AVAILABLE:
            self.processing_error.emit(
                "OpenAI API Not Available",
                "The OpenAI package is not installed. Please install it with 'pip install openai'."
            )
            return
        
        # Create a worker thread for the preview
        class PreviewWorker(QThread):
            preview_ready = Signal(str)
            preview_error = Signal(str, str)
            
            def __init__(self, settings, text, voice, model, instructions):
                super().__init__()
                self.settings = settings
                self.text = text
                self.voice = voice
                self.model = model
                self.instructions = instructions
            
            def run(self):
                try:
                    # Initialize OpenAI client
                    client = OpenAI(api_key=self.settings.api_key)
                    
                    # Create temp file
                    preview_file = os.path.join(
                        self.settings.temp_dir,
                        f"preview_{int(time.time())}.{self.settings.output_format}"
                    )
                    
                    # Generate speech
                    try:
                        # Create parameters for the API call
                        params = {
                            "model": self.model,
                            "voice": self.voice,
                            "input": self.text,
                            "response_format": self.settings.output_format
                        }
                        
                        # Only add instructions parameter for models that support it
                        # and only if instructions are provided
                        if self.model == "gpt-4o-mini-tts" and self.instructions:
                            try:
                                # Try with instructions parameter
                                with client.audio.speech.with_streaming_response.create(
                                    **params,
                                    instructions=self.instructions
                                ) as response:
                                    response.stream_to_file(preview_file)
                            except Exception as e:
                                if "unexpected keyword argument 'instructions'" in str(e):
                                    # Fall back to without instructions if not supported
                                    response = client.audio.speech.create(**params)
                                    response.stream_to_file(preview_file)
                                else:
                                    raise
                        else:
                            # For older models or when no instructions are provided
                            response = client.audio.speech.create(**params)
                            response.stream_to_file(preview_file)
                    except Exception as e:
                        # Handle specific API errors
                        error_msg = str(e)
                        if "unexpected keyword argument 'instructions'" in error_msg:
                            self.preview_error.emit(
                                "API Error",
                                f"There was an error using instructions with the model '{self.model}'. This might be due to an API version mismatch or the OpenAI client library not supporting this feature yet."
                            )
                        else:
                            # Re-raise other exceptions
                            raise
                    
                    # Signal completion
                    self.preview_ready.emit(preview_file)
                    
                except Exception as e:
                    self.preview_error.emit("Preview Error", f"Error generating preview: {str(e)}")
        
        # Create and start worker
        worker = PreviewWorker(self.settings, text, voice, model, instructions)
        worker.preview_ready.connect(self.preview_ready)
        worker.preview_error.connect(self.processing_error)
        worker.start()
        
        # Store reference to prevent garbage collection
        self._preview_worker = worker