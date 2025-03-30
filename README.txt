# CSV to TTS Converter
![UI](https://github.com/juangrukat/csvtts/blob/main/csvtts.png)
A desktop application for converting text from CSV files to speech using OpenAI's Text-to-Speech API.

## Overview

CSV to TTS Converter is a user-friendly tool that allows you to:
- Load CSV files and select specific columns containing text to convert
- Generate high-quality speech audio using OpenAI's TTS API
- Process individual files or batch process multiple CSV files
- Preview audio before processing large files
- Export generated audio files to a location of your choice

## Features

- **CSV File Support**: Load and process standard CSV files
- **Column Selection**: Choose which column contains the text you want to convert
- **Multiple Voice Options**: Select from various OpenAI voices (alloy, echo, fable, onyx, nova, shimmer, coral, ash, ballad, sage)
- **Model Selection**: Choose between different TTS models (tts-1, tts-1-hd, gpt-4o-mini-tts)
- **Voice Instructions**: Add custom instructions for voice style (accent, emotion, etc.) when using gpt-4o-mini-tts model
- **Batch Processing**: Process multiple CSV files in a directory at once
- **Audio Preview**: Generate and play a preview of the TTS output before processing
- **Export Options**: Export all processed files to a directory of your choice
- **Multiple Output Formats**: Support for mp3, opus, aac, and flac audio formats

## Requirements

- Python 3.6 or higher
- PySide6 (Qt for Python)
- OpenAI Python package
- An OpenAI API key with access to the TTS API

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python mainwindow.py
   ```

## Usage

### Basic Usage

1. **Set up your API Key**:
   - Go to Settings > Preferences
   - Enter your OpenAI API key
   - Adjust other settings as needed

2. **Load a CSV File**:
   - Click the "Browse" button to select a CSV file
   - The application will display a preview of the file contents

3. **Select Text Column**:
   - Choose which column contains the text you want to convert to speech

4. **Choose Voice and Model**:
   - Select your preferred voice from the dropdown menu
   - Select the TTS model to use
   - For gpt-4o-mini-tts model, you can add custom instructions for voice style

5. **Set Output Directory**:
   - Click "Browse" next to the output directory field to select where to save the audio files

6. **Process the File**:
   - Click "Process" to convert the text to speech
   - The progress bar will show the conversion progress

### Batch Processing

1. **Enable Batch Mode**:
   - Check the "Batch Processing" checkbox

2. **Set Output Directory**:
   - Select an output directory for all generated files

3. **Process Files**:
   - Click "Batch Process" to process all CSV files in the same directory as your selected file

### Preview

- Click the "Preview" button to generate and play a sample of the TTS output
- For long texts, you'll be asked if you want to preview only the first 500 characters

### Export

- After processing, click "Export All" to save all generated audio files to a directory of your choice
- The application will open the export directory when complete

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is valid and has access to the TTS API
- **File Format Issues**: Make sure your CSV files are properly formatted with headers
- **Processing Errors**: Check the error messages for specific issues with the API or file processing

## License

This software is provided as-is without any warranty. Use at your own risk.

## Credits

Developed using PySide6 and OpenAI's TTS API.