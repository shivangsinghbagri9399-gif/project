# Chapter 5 — Benefits

## 5.1 Educational benefits

The program gives a concrete example of converting a human-readable string to bytes and modifying image samples. Students can compare input/output pixels and inspect the exact bit-level operations. Learning outcomes have not been measured.

## 5.2 Software engineering benefits

The implementation exposes a complete desktop path from user event through input validation, processing, file output, and feedback. It also illustrates how a monolithic source file can still contain identifiable functional responsibilities. Separation into an algorithm module and UI module would improve maintainability as scope grows.

## 5.3 Cybersecurity learning

The app demonstrates concealment while creating a useful opportunity to discuss why concealment is not encryption. Its fixed, keyless format is a practical example of a design that should not be relied on for confidential communication.

## 5.4 Image-processing learning

Converting images to RGB and traversing pixel tuples demonstrates a sample-domain manipulation. Alpha and metadata are not preserved explicitly, which also illustrates that format conversion can have consequences beyond the visible RGB appearance.

## 5.5 Algorithm understanding

The 32-bit length prefix illustrates framing: the receiver learns how many payload bits to read. MSB-first shifts and masks make bit order observable and testable.

## 5.6 GUI development

Tkinter demonstrates windows, themed controls, event callbacks, file dialogs, and widget state. The GUI is not automated-tested, so its runtime usability is not established by the test result.

## 5.7 Testing

The test script uses temporary directories and generated images, avoiding dependence on a valid sample fixture for its cases. Its categories are useful but limited; tests are direct script functions rather than framework-managed tests.

## 5.8 Maintainability

The algorithm helpers have clear names and a short dependency chain, but UI and algorithm logic share `steg_app.py`. The existing documentation needs alignment with code: it claims PNG-only validation, includes stale capacity estimates, and the provided placeholder image is empty.

## 5.9 Portability

Python and Pillow are broadly available, while Tkinter depends on the Python distribution and platform GUI environment. The current test establishes behavior only in the workspace’s Python 3.14.4/Pillow 12.3.0 environment, not across operating systems.

## 5.10 Cost

No paid runtime, hosted service, or database is required by the source. The dependency manifest contains only Pillow; Tkinter is part of Python’s standard-library interface, though an OS package may be required on some installations. No formal deployment cost study exists.

## 5.11 Demonstration

The encode/decode flow can be shown with a generated RGB PNG and a short message. `samples/placeholder.png` cannot currently serve this purpose because it has zero bytes.

## 5.12 Research value

The code can serve as a baseline for future experiments on payload size, distortion, detection, and robustness. Those experiments must be run and documented before conclusions about image quality or security can be drawn.
