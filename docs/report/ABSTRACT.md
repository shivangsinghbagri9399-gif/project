# Abstract

**Implementation note:** This report describes the earlier desktop-only version. The current Streamlit web app also supports optional password-based authenticated encryption before embedding; the Tkinter desktop interface remains plaintext-only.

The LSB Steganography Mini-App is a local Python desktop program for embedding and recovering UTF-8 text in image samples by replacing least significant bits (LSBs) in RGB channel values. It addresses an educational problem: demonstrating how text bytes, image pixels, and a reversible bit-level transformation can be connected in an interactive program, while making clear that data hiding is not cryptographic confidentiality.

The implementation is a single Python module. Its Tkinter interface provides Encode and Decode tabs; Pillow opens image files, converts them to RGB, traverses pixel data, and writes the encoded result. The encoder prefixes the payload with a 32-bit, most-significant-bit-first integer containing the payload length in **bits**, then writes each UTF-8 payload byte most-significant bit first into the R, G, and B LSBs of pixels in row-major order. The decoder reads that header, checks alignment and image capacity, reconstructs bytes, and decodes with UTF-8 error handling set to `ignore`. The encoded output is saved as a new RGB PNG path derived from the selected input path.

The workspace test script has four test functions covering an ordinary round trip, rejection of an oversized message, a Unicode round trip, and three image dimensions. Running the script in the configured Python 3.14.4 virtual environment with Pillow 12.3.0 produced **4 passed, 0 failed**. This result is limited to those checks: the GUI was not exercised, no performance benchmark or image-quality metric was collected, and the repository’s `samples/placeholder.png` is a zero-byte file rather than a usable image.

The implementation is intentionally simple and keyless. Its predictable sequential embedding is vulnerable to inspection and statistical steganalysis; any observer with the image and algorithm can attempt extraction. There is no encryption, authentication, integrity check, payload magic value, or recovery mechanism. Re-saving through a lossy or otherwise pixel-changing transformation may corrupt the message. The project’s contribution is therefore a reproducible teaching example and an inspectable implementation of spatial-domain LSB embedding, not a secure communication channel.

**Keywords:** image steganography; LSB; RGB; UTF-8; Pillow; Tkinter; capacity; security analysis.
