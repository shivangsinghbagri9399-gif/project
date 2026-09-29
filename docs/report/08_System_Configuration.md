# Chapter 8 — System Configuration

## 8.1 Hardware

No hardware minimum is declared by the project. The algorithm is CPU-based and uses memory proportional to image pixels and payload bits. Actual suitability depends on image dimensions and available memory; no minimum processor/RAM benchmark was established.

## 8.2 Software and operating system

The configured workspace ran macOS with a Python virtual environment. OS version is not recorded. Source includes Tkinter, which requires a compatible Tcl/Tk installation. Cross-platform compatibility is plausible but not verified by this test evidence.

## 8.3 Python and dependencies

The configured local environment reports Python 3.14.4 and Pillow 12.3.0. The only runtime dependency in [requirements.txt](../../requirements.txt) is `pillow>=10.0.0`. Tkinter and supporting imports are from the standard library. `python-docx` is imported by the legacy report generator but not listed and is not required to execute the application or test script.

## 8.4 Python

The workspace virtual environment reports Python 3.14.4. The repository does not declare a minimum version or supported-version matrix, so Python 3.14.4 is an observed test environment rather than a formal project requirement.

## 8.5 Dependencies

Pillow is the only dependency in `requirements.txt`, specified as `pillow>=10.0.0`. Tkinter is imported from the Python standard library but may require a platform-specific Tk installation. `python-docx` is used only by the legacy DOCX generator and is not declared in the application requirements.

## 8.6 Installation

The project README documents these commands:

```bash
pip install -r requirements.txt
python steg_app.py
```

The test script can be run with:

```bash
python test_steg.py
```

These command forms match the repository documentation. This report’s test evidence was obtained with the workspace environment’s explicit Python path, not a newly created clean installation.

## 8.7 Configuration

There is no configuration file, environment-variable contract, database, or credentials file. Output path is derived from the selected input filename. GUI dimensions and styling are constants in `StegApp.__init__`.

## 8.8 Directory structure

```text
.
├── steg_app.py
├── test_steg.py
├── requirements.txt
├── README.md
├── docs/
│   ├── usage.md
│   └── report/                 # This report source
├── samples/
│   ├── example_message.txt
│   └── placeholder.png         # Empty, not a usable image
├── generate_report.py         # Legacy python-docx report generator
├── project_report.docx        # Existing generated artifact
├── project-diagram.png
└── LSB_Steganography_Mini-App_Project_Synopsis.md
```

This is the relevant tracked project structure; installed packages in `.venv` are environment contents, not application modules.

## 8.9 Execution

Run the desktop app with `python steg_app.py`; run the project’s standalone test script with `python test_steg.py`. These commands are documented in the README and the test invocation was run successfully using the configured virtual environment’s Python executable.

## 8.10 Input requirements

The GUI accepts files whose suffix is one of `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.webp`, `.tif`, `.tiff`, or `.jfif`, provided Pillow can decode the content. Encoding also requires a non-whitespace single-line text entry. For predictable LSB preservation, use a lossless carrier and avoid transformations after encoding.

## 8.11 Output behavior

Encoding writes `<input stem>_encoded.png` to the same directory as the input. Decoding displays recovered text in the GUI and does not write it to a separate file. Metadata and alpha are not explicitly preserved through RGB conversion.

## 8.12 Environment reproducibility

The local verified environment is Python 3.14.4 with Pillow 12.3.0 on macOS. No lockfile or OS/Tk version record is included. The test script creates images itself, while the sample placeholder file is empty. A reproducible environment beyond this observed setup requires pinning Python/dependencies and documenting Tk availability.

## I/O contract summary

| Operation | Input | Transformation | Output |
|---|---|---|---|
| Encode | Existing image file with accepted suffix; non-whitespace text | Decode image, RGB conversion, UTF-8, length header, RGB LSB replacement | `<input stem>_encoded.png` in same directory; source file is not intentionally overwritten |
| Decode | Existing image file with accepted suffix | RGB conversion, header and payload extraction, UTF-8 decode with `errors="ignore"` | Message displayed in GUI; no recovered-message file is written |

The UI’s labels mention PNG, but its extension allowlist is broader. Image content validity ultimately depends on Pillow.

The tests generate their own RGB PNGs and do not depend on sample files. The tracked sample placeholder is zero bytes, confirmed by file inspection and Pillow’s `UnidentifiedImageError`. A fresh user should generate a valid PNG or use another readable image rather than rely on that file.
