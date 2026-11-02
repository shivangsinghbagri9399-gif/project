# Usage Guide

## Quick Start

### 1. Encoding a Message

1. **Select an image**: Use "Browse Photo" in the Encode tab to choose a readable file with a supported extension. PNG is recommended because it is lossless.
2. **Enter your secret**: Type the message you want to hide in the text box.
3. **Encode and Save**: Click "Encode → Save" to create the steganographic image.
4. **Verify success**: A confirmation message will show the filename of the saved image.

### 2. Decoding a Message

1. **Select an image**: Use "Browse..." in the Decode tab to choose the image containing hidden data.
2. **Extract the message**: Click "Decode → Show" to retrieve the hidden text.
3. **View the result**: The decoded message will appear in the text area below.

## Encryption in the web app

In the Streamlit Encode tab, encryption is enabled by default. The default method generates a separate key file, so no password is required: download and keep the `.key` file separate from the PNG. On decode, first upload and decode the image, then upload its matching key file when prompted. You can instead choose password encryption and enter a strong passphrase, or turn encryption off. The app detects encrypted payloads automatically. Images encoded without encryption still decode without a key. Lost passwords and key files cannot be recovered, and encryption overhead reduces image capacity.

## Best Practices

### Image Selection
- **Format**: PNG is recommended due to its lossless compression; the GUI accepts PNG, JPG/JPEG/JFIF, BMP, GIF, WebP, and TIFF extensions
- **Size**: Larger images provide more storage capacity
- **Preservation**: Avoid resizing, filtering, color conversion, or lossy re-encoding after embedding; these can corrupt LSB data

### Message Length Guidelines
- **100×100 RGB**: 3,746 whole payload bytes after the 32-bit length header
- **500×500 RGB**: 93,746 whole payload bytes
- **1000×1000 RGB**: 374,996 whole payload bytes

These are UTF-8 byte capacities, not guaranteed character counts.

## Troubleshooting

### "Image is too small" Error
- **Solution**: Use a larger image or shorten your message
- **Tip**: Try splitting large messages across multiple images

### Unsupported file extension
- **Solution**: Select a file with an extension in the GUI's supported image filter; the image must also be readable by Pillow

### No Message Extracted
- **Cause**: Image wasn't encoded with this application
- **Fix**: Re-encode or try a different image

### Visual and security limitations
The encoder changes RGB least significant bits, with each changed channel varying by at most one intensity level. This alone does not establish perceptual invisibility or resistance to steganalysis. Streamlit encrypts messages by default with a separate key file, with password and plaintext modes available. Encrypted messages are authenticated. The desktop GUI does not currently offer encryption.
