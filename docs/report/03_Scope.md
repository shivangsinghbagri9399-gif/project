# Chapter 3 — Scope

## 3.1 Functional scope

The program offers GUI-driven image path selection, one-line message input, encoding to a derived PNG path, decoding from a selected supported-extension file, and displaying extracted text. The reusable functions can also be called directly without constructing the GUI.

## 3.2 Technical scope

Implementation is limited to Python, Tkinter, Pillow, and in-memory RGB sample manipulation. There is no network service, database, command-line interface beyond starting the GUI or test script, or formal plugin/module architecture.

## 3.3 User scope

The controls target a single interactive desktop user. Accounts, roles, multi-user workflows, and access controls are absent. No usability study or supported user profile is documented.

## 3.4 Image scope

The browse filter and extension check accept PNG, JPG/JPEG/JFIF, BMP, GIF, WebP, and TIFF suffixes. Actual readability depends on Pillow and file contents. Both encode and decode convert opened images to RGB. The encoder writes PNG; it does not preserve alpha or explicitly preserve metadata. The project documentation’s PNG-only statements are narrower than the actual extension check.

## 3.5 Message scope

The functional API accepts a Python string and converts it to UTF-8. The GUI entry is single-line and rejects whitespace-only input. There is no file-payload embedding, arbitrary binary payload API, message encryption, or explicit maximum-message widget. Capacity is measured in UTF-8 **bytes**, not Unicode characters.

## 3.6 Platform scope

The project declares Python 3.x in its existing docs but no minimum Python version. The inspected workspace contains a Python 3.14.4 virtual environment on macOS. Cross-platform behavior is not established by test evidence.

## 3.7 Security scope

The project demonstrates concealment through fixed sequential LSB replacement. It does not implement cryptographic confidentiality, keying, integrity/authentication, steganalysis resistance, secure deletion, or adversarial robustness.

## 3.8 Testing scope

The test script covers ordinary ASCII round-trip, an oversized message, a Unicode string, and three image dimensions using generated solid-color RGB PNGs. The GUI, corrupted carriers, invalid header branches, exact capacity boundary, input extension matrix, and visual quality are not tested.

## 3.9 Research scope

The report gives an implementation-derived model, complexity and capacity analysis, and threat discussion. It does not report experimental PSNR/SSIM, runtime benchmarks, steganalysis results, or comparative algorithm performance.

## 3.10 Current limitations

Current limitations include:

- sequential, fixed, unkeyed embedding;
- no magic identifier, checksum, authentication, or error correction;
- UTF-8 decode uses `errors="ignore"`, which can silently remove invalid bytes;
- unrecognized images with a plausible length header may yield arbitrary text;
- resizing, cropping, filtering, palette changes, or lossy encoding can disrupt recovery;
- full pixel and bit lists are materialized in memory;
- the sample `samples/placeholder.png` is empty;
- README and usage guidance contain inaccurate capacity examples and PNG-only wording;
- GUI and performance are not covered by the current tests.

## 3.11 Excluded features

Encryption, password protection, keyed/permuted embedding, adaptive embedding, transform-domain processing, compression, error correction, file attachments, networking, batch processing, database persistence, progress reporting, and steganalysis are not present.

## 3.12 Future research scope

Future work could compare keyed and content-adaptive schemes, add authenticated encryption and a versioned payload header, test robustness against explicit transformations, measure image distortion and detection rates, reduce allocation overhead, and automate GUI tests. Such features must be labeled as future work until implemented and validated.

**Traceability:** [steg_app.py](../../steg_app.py#L149), [test_steg.py](../../test_steg.py), [README.md](../../README.md), [docs/usage.md](../usage.md), [samples/placeholder.png](../../samples/placeholder.png).
