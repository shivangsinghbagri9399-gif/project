# LSB Steganography Mini-App

A simple desktop application built with Python Tkinter that allows you to hide text messages inside image samples using Least Significant Bit (LSB) steganography, and later recover them. The GUI accepts several image file extensions, converts decoded input to RGB, and saves encoded output as PNG.

## Features

- **Encode Tab**: Select a supported image, enter a secret message, and save a new PNG image with the hidden message
- **Decode Tab**: Select an image that contains a hidden message and extract the text
- **User-Friendly Interface**: Clean, simple layout suitable for beginners
- **Feedback System**: Clear status messages for success and error conditions
- **PNG Output**: Encoded output is saved as PNG; use lossless images and do not resize, filter, or convert the encoded file if you need to recover the message

## Requirements

- Python 3.x
- Pillow library (PIL fork)

## Installation

1. Clone or download this repository
2. Install the required dependency:
   ```bash
   pip install -r requirements.txt
   ```
   or manually:
   ```bash
   pip install pillow
   ```

## Usage

1. Run the application:
   ```bash
   python steg_app.py
   ```

2. **To Encode a Message**:
   - Go to the "Encode" tab
   - Click "Browse Photo" to select an image with a supported extension
   - Type your secret message in the text box
   - Click "Encode → Save"
   - The application will save a new PNG image with "_encoded" suffix containing your hidden message

3. **To Decode a Message**:
   - Go to the "Decode" tab
   - Click "Browse..." to select an image that contains a hidden message
   - Click "Decode → Show"
   - The hidden message will appear in the text box below

## How It Works

This application uses Least Significant Bit (LSB) steganography:
- It modifies the least significant bit of each color channel (Red, Green, Blue) in the image pixels
- These changes are visually imperceptible but can store binary data
- A 32-bit length prefix is added to know where the message ends
- The message is encoded in UTF-8 format

## Capacity Calculation

Each RGB pixel supplies 3 channel LSBs. The first 32 bits store payload length in bits:
- Total channel slots = image_width × image_height × 3
- Payload capacity in bits = total channel slots - 32
- Maximum whole UTF-8 payload bytes = floor(payload capacity in bits / 8)

For example, a 100×100 RGB image provides:
- (100 × 100 × 3 - 32) / 8 = 3,746 whole payload bytes

This is a byte limit, not necessarily a character limit: UTF-8 characters can use multiple bytes. The implementation is educational and does not encrypt or authenticate the message.

## Notes

- **PNG Recommended**: Use PNG format as it's lossless and won't compress away the hidden data
- **JPEG Warning**: JPEG compression will destroy the hidden data due to its lossy nature
- **File Size**: The encoded image will be the same size as the original
- **Security**: This is for educational purposes only - not suitable for serious cryptographic security

## Troubleshooting

- **"Image is too small" error**: Try a larger image or a shorter message
- **Unsupported image extension**: Select a file with one of the extensions accepted by the GUI; Pillow must still be able to read the file
- **No message extracted**: Make sure you're using an image that was actually encoded with this application

## Technical Report

The implementation-grounded technical report, including the algorithm analysis, system diagrams, security limitations, and executed test evidence, is available in [PROJECT_REPORT.md](PROJECT_REPORT.md). Its modular chapter sources and report builder are in [`docs/report/`](docs/report/).

## License

This project is open source and available for personal and educational use.

---

*Built with Python Tkinter and Pillow*