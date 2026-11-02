# LSB Steganography App

A desktop and web application that hides text messages inside images using Least Significant Bit (LSB) steganography, and can recover them later. The web interface is built with Streamlit; both interfaces save encoded output as PNG.

## Features

- **Encode Tab**: Select a supported image, enter a secret message, and save a new PNG image with the hidden message
- **Decode Tab**: Select an image that contains a hidden message and extract the text
- **User-Friendly Interface**: Clean, simple layout suitable for beginners
- **Feedback System**: Clear status messages for success and error conditions
- **PNG Output**: Encoded output is saved as PNG; use lossless images and do not resize, filter, or convert the encoded file if you need to recover the message
- **Web App**: Use the browser-based interface to encode and decode images

## Requirements

- Python 3.x
- Tkinter for the desktop app
- Pillow library (PIL fork)
- Streamlit for the web app

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

### Desktop app

1. Start the application:
   - On Windows, double-click `run.bat`. It installs the required packages on first run if needed.
   - On macOS, double-click `run.command`. It creates a local Python environment and installs Pillow on first run if needed. If Tkinter is missing, install Python from [python.org](https://www.python.org/downloads/macos/) and try again. If macOS blocks the launcher, right-click it, choose **Open**, and confirm.
   - Or run it manually:
     ```bash
     python steg_app.py
     ```

### Web app

Install dependencies and run locally:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

#### Free online deployment with Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub.
3. Choose **Create app**, select the repository and branch, and set the app file to `app.py`.
4. Deploy; Streamlit will install packages from `requirements.txt` and provide a shareable URL.

The web app processes uploaded images in memory and does not intentionally save them. A public deployment is still not appropriate for private images or sensitive messages; this tool does not encrypt or authenticate content.

### Using the app

1. **To Encode a Message**:
   - Open the Encode tab
   - Select a cover image with a supported extension
   - Type your secret message in the text box
   - Click the encode button and download the resulting PNG

2. **To Decode a Message**:
   - Open the Decode tab
   - Select an image that contains a hidden message
   - Click the decode button to show the extracted text

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