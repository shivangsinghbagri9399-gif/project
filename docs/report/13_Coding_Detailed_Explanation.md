# Chapter 13 — Coding with Detailed Explanation

This chapter maps statements to the current [steg_app.py](../../steg_app.py) implementation. Names that are absent from the code are not treated as implemented functionality.

## 13.1 Imports and entry point

Imports are `os`, `tkinter`, selected Tkinter dialogs/widgets/variables, and `PIL.Image`/`ImageTk`. The app path uses `os` and Tkinter plus `Image`; tests import the two main processing functions. `messagebox`, `IntVar`, `ImageTk`, and the conversion helpers `rgb_to_bytes` / `int_to_rgb` are present but unused in the current path.

The guarded entry point is:

```python
if __name__ == "__main__":
    app = StegApp()
    app.mainloop()
```

This keeps the GUI from opening when the module is imported by `test_steg.py`.

## 13.2 `rgb_to_bytes(r, g, b)`

```python
def rgb_to_bytes(r, g, b):
    return (r << 16) | (g << 8) | b
```

**Purpose:** Pack three channel integers into one 24-bit integer as `(r << 16) | (g << 8) | b`.

**Operational types/return:** Three integer-like channel values; returns `int`. No annotations or runtime type/range checks exist in source.

**Callers:** None in the inspected project.

**Complexity:** Constant time and constant additional space. This helper is unused by the embedding format and should not be mistaken for payload serialization.

## 13.3 `int_to_rgb(value)`

```python
def int_to_rgb(value):
    return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)
```

**Purpose:** Extract high, middle, and low 8-bit fields using right shifts and mask `0xFF`.

**Operational types/return:** Integer-like input → 3-tuple of integers. No annotations or validation that the input fits 24 bits; masks discard higher bits.

**Callers:** None in the inspected project. Complexity is O(1) time and space.

## 13.4 `extract_bits_from_image(image)`

```python
def extract_bits_from_image(image):
    for pixel in image.getdata():
        if len(pixel) == 3:
            r, g, b = pixel
            yield r & 1
            yield g & 1
            yield b & 1
        elif len(pixel) == 4:
            r, g, b, _ = pixel
            yield r & 1
            yield g & 1
            yield b & 1
        else:
            for channel in pixel[:3]:
                yield channel & 1
```

The generator iterates `image.getdata()`. For a 3-element pixel it yields `r & 1`, `g & 1`, `b & 1`. For a 4-element tuple it yields RGB and ignores alpha. Otherwise it yields up to the first three tuple items.

**Operational types/return:** Pillow image → lazy iterator yielding integers in `{0,1}`. The generator itself uses O(1) additional state beyond the image held by Pillow. Source has no annotations.

**Callers:** `extract_message` invokes this helper twice. Its normal path converts the image to RGB first, so special tuple branches do not ordinarily run through that caller.

**Edge note:** For a grayscale pixel represented as a scalar rather than a tuple, `len(pixel)` would fail; however, conversion to RGB in the caller avoids this. The helper is therefore not generally mode-independent despite its fallback comment.

## 13.5 `embed_bits_into_image(image, bits, max_bits)`

**Purpose:** Replace up to three channel LSBs per RGB-like pixel, then construct an image containing changed and unchanged pixels.

**Operational inputs/return:** Pillow image; materialized sequence/list of integer bits; integer maximum; returns Pillow image. There are no type annotations or validation that each bit is 0 or 1.

Core embedding loop from the implementation:

```python
new_pixels = []
bit_iter = iter(bits)
for pixel in image.getdata():
    if len(pixel) >= 3:
        r, g, b = pixel[:3]
        r = (r & 0xFE) | next(bit_iter, 0)
        g = (g & 0xFE) | next(bit_iter, 0)
        b = (b & 0xFE) | next(bit_iter, 0)
        new_pixel = list(pixel)
        new_pixel[:3] = (r, g, b)
        new_pixels.append(tuple(new_pixel))
    else:
        new_pixels.append(pixel)
    if len(new_pixels) * 3 >= len(bits):
        break
```

**Control flow:**

1. Raise `ValueError` when `len(bits) > max_bits`.
2. Iterate source pixels.
3. For tuple length at least three, take first three values as RGB, replace their LSBs via `(channel & 0xFE) | next(bit_iter, 0)`, preserve additional tuple fields, append the tuple.
4. For shorter tuples, append unchanged.
5. Stop when `len(new_pixels) * 3 >= len(bits)`.
6. Materialize the original pixel iterator again as `raw`, append remaining untouched pixels.
7. Create an image using original mode and size; `putdata(new_pixels)`.

**Output:** New Pillow image, not saved here.

**Complexity:** Let `P=WH` and `B=len(bits)`. The traversal copies approximately `ceil(B/3)` pixels for an RGB image (bounded by `P`); then it materializes all `P` pixels again and constructs an output list of `P` pixel tuples. Thus time is O(P+B), and additional Python-level storage is O(P+B) including `bits`, `raw`, and `new_pixels`; the Pillow output image itself is also O(P). The call site supplies RGB and valid capacity, so the generic short-pixel issue does not affect normal use.

**Error behavior:** `max_bits` is a count guard, but it does not validate bit values. Unexpected tuple sizes/modes may produce behavior not exercised by tests.

## 13.6 `hide_message(image_path, message, output_path)`

**Purpose:** Encode UTF-8 text into an image and save the result.

**Operational parameters/return:** `image_path: str` path, `message: str`, `output_path: str` path; returns a Pillow image after saving. These are observed usage contracts; source has no type annotations.

Source implementation:

```python
def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    capacity_bits = width * height * 3

    msg_bytes = message.encode("utf-8")
    msg_len_bits = len(msg_bytes) * 8
    if msg_len_bits > capacity_bits - 32:
        raise ValueError("Image is too small to hold this message.")

    length_bits = [(msg_len_bits >> i) & 1 for i in range(31, -1, -1)]
    msg_bits = [
        (msg_bytes[j // 8] >> (7 - (j % 8))) & 1
        for j in range(len(msg_bytes) * 8)
    ]
    bits = length_bits + msg_bits

    stego_img = embed_bits_into_image(img, bits, capacity_bits)
    stego_img.save(output_path)
    return stego_img
```

**Algorithm and control flow:**

1. `Image.open(image_path).convert("RGB")`.
2. Calculate `capacity_bits = width * height * 3`.
3. Encode string with UTF-8; compute `msg_len_bits = len(msg_bytes)*8`.
4. Raise `ValueError` if `msg_len_bits > capacity_bits - 32`.
5. Build header list using shifts 31 down to 0.
6. Build payload bit list using byte index `j//8` and bit offset `7-(j%8)`.
7. Concatenate header and payload lists.
8. Call `embed_bits_into_image(img, bits, capacity_bits)`.
9. Save output image and return it.

Header and payload bit generation in the source:

```python
length_bits = [(msg_len_bits >> i) & 1 for i in range(31, -1, -1)]
msg_bits = [
    (msg_bytes[j // 8] >> (7 - (j % 8))) & 1
    for j in range(len(msg_bytes) * 8)
]
bits = length_bits + msg_bits
```

**Header semantics:** Unsigned 32-bit field contains payload bit count. Python integers are unbounded; no separate guard ensures the count fits in 32 bits. In practice, allocating a string large enough to exceed this is constrained by memory, but the format formally has a 32-bit limit that the code does not explicitly enforce.

**Complexity:** For `P=WH` and `M` UTF-8 bytes, bit construction is O(M), image access/output is O(P), and total time is O(P+M); memory is O(P+M), with bit-list overhead larger than packed bytes. No benchmark was run.

**Errors:** Pillow open/convert/save failures propagate; capacity failure is a `ValueError`. Empty text has zero payload bits and core helper can encode a 32-bit zero header, though the GUI blocks whitespace-only strings.

## 13.7 `extract_message(stego_path)`

**Purpose:** Recover the length-prefixed byte payload.

**Operational parameter/return:** Image path string → Python `str`; no source annotations.

Source implementation:

```python
def extract_message(stego_path):
    img = Image.open(stego_path).convert("RGB")
    width, height = img.size
    capacity_bits = width * height * 3
    if capacity_bits < 32:
        raise ValueError("Image is too small to contain a hidden message.")

    length_bits = []
    bit_iter = extract_bits_from_image(img)
    for _ in range(32):
        length_bits.append(next(bit_iter, 0))

    message_len_bits = 0
    for bit in length_bits:
        message_len_bits = (message_len_bits << 1) | bit

    if message_len_bits % 8:
        raise ValueError("The encoded message length is invalid.")
    if message_len_bits > capacity_bits - 32:
        raise ValueError("The image does not contain a valid hidden message.")

    total_bits_to_read = 32 + message_len_bits
    needed_bits = []
    bit_iter = extract_bits_from_image(img)
    for _ in range(total_bits_to_read):
        needed_bits.append(next(bit_iter, 0))

    message_bytes = []
    for i in range(0, message_len_bits, 8):
        byte = 0
        for j in range(8):
            if i + j < len(needed_bits):
                byte |= needed_bits[32 + i + j] << (7 - j)
        message_bytes.append(byte)

    return bytes(message_bytes).decode("utf-8", errors="ignore")
```

The corresponding header validation and byte reconstruction use:

```python
if message_len_bits % 8:
    raise ValueError("The encoded message length is invalid.")
if message_len_bits > capacity_bits - 32:
    raise ValueError("The image does not contain a valid hidden message.")

message_bytes = []
for i in range(0, message_len_bits, 8):
    byte = 0
    for j in range(8):
        if i + j < len(needed_bits):
            byte |= needed_bits[32 + i + j] << (7 - j)
    message_bytes.append(byte)
message = bytes(message_bytes).decode("utf-8", errors="ignore")
```

**Algorithm:**

1. Open and convert image to RGB.
2. Compute `capacity_bits=3WH`; reject if less than 32.
3. Read 32 yielded LSB values into `length_bits`.
4. Fold bits into `message_len_bits` with left shift and OR.
5. Reject if bit length is not divisible by 8.
6. Reject if length exceeds `capacity_bits-32`.
7. Create a new iterator, collect exactly `32+message_len_bits` bits.
8. For each 8-bit payload group, OR bits into an integer with shifts `7-j`.
9. Build bytes and decode UTF-8 with `errors="ignore"`.

The header integer is reconstructed by the actual loop:

```python
message_len_bits = 0
for bit in length_bits:
    message_len_bits = (message_len_bits << 1) | bit
```

**Complexity:** For image size `P` and decoded message byte count `M`, RGB conversion and `getdata()` traversal are O(P); it traverses up to `32+8M` bits twice (once for header, again for complete stream), and byte reconstruction is O(M). Total time is O(P+M). It stores a header list, a full needed-bit list O(M), and a byte list O(M), in addition to the decoded Pillow image O(P). Peak additional space is O(P+M).

**Error/validation limits:** Header capacity, alignment, and upper bound are checked. No magic/version/checksum is checked. `errors="ignore"` can turn corrupted bytes into truncated or altered text without an exception. A non-stego image whose first 32 LSBs decode to a valid small length can return arbitrary text.

## 13.8 `StegApp` class

`StegApp` subclasses `tk.Tk`. It centralizes the widget tree and the two user callbacks.

### `__init__(self)`

Sets the title, geometry `620x500`, minimum `580x420`, resize behavior, style settings, and invokes notebook/Encode/Decode construction. No file processing occurs during initialization.

### `_is_supported_image(path)`

Operationally accepts a path string and returns `bool`. Returns false for empty/non-file paths; otherwise lowercases the suffix and checks an allowlist: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.webp`, `.tif`, `.tiff`, `.jfif`. It checks a filename suffix, not the image’s actual format. Source has no annotation.

### `_create_notebook(self)`

Creates a `ttk.Notebook` in the root and packs it to fill/expand.

### `_create_enc_tab(self)`

Creates a frame and Encode tab; adds labels, a path `StringVar` and entry, nested browse callback, message `StringVar` and entry, encode button callback, and feedback label. Uses `grid` geometry manager inside the frame.

### `_create_dec_tab(self)`

Creates Decode controls similarly, plus a disabled `tk.Text` output. Decode output is temporarily enabled to clear/insert content, then made disabled again by callback.

### `_encode(self)`

Reads GUI path/message; rejects invalid path or whitespace-only content; derives output path using the final period split; calls `hide_message`; updates feedback. Broad `except Exception` turns failures into a string label. It does not use imported `messagebox`.

### `_decode(self)`

Validates path; calls `extract_message`; updates text widget and status. On exception it displays the error both in feedback and the text area. Error details are shown without a structured error taxonomy.

## 13.9 GUI architecture and event flow

Tkinter event callbacks run on the GUI thread. A large image may therefore make the interface appear unresponsive while processing. There is no background thread, task cancellation, or progress indicator. This is a design observation from the synchronous callbacks; timing was not measured.

## 13.10 Test functions

The test function contracts and actual outcomes are tabulated in [Chapter 15](./15_Software_Testing.md). Tests call `hide_message`/`extract_message` directly and do not instantiate `StegApp`.

## 13.11 Test and auxiliary module functions

| Function | Operational parameters and return | Algorithm / role |
|---|---|---|
| `create_test_image(width=200, height=200)` | Integer dimensions → Pillow RGB image | Creates solid `(100,150,200)` image using `Image.new`. |
| `test_encode_decode()` | No explicit args → `bool` | Creates temporary files, encodes a fixed ASCII message, checks output exists and extracted text equality. |
| `test_capacity_limits()` | No explicit args → `bool` | Attempts 100 ASCII bytes in 10×10 RGB; passes only if `ValueError` is raised. |
| `test_utf8_support()` | No explicit args → `bool` | Encodes and compares one string containing multiple scripts and an emoji. |
| `test_multiple_images()` | No explicit args → `bool` | Iterates three dimensions and returns false on first mismatch/error; true after all. |
| `set_doc_style(doc)` | `python-docx` Document → `None` | Sets Times New Roman, 12-point font, paragraph spacing, and line spacing. |
| `add_centered(doc,text,bold=False,size=12)` | Document, string, bool, number → paragraph | Appends centered paragraph/run and returns paragraph. |
| `add_section_title(doc,title,level=1)` | Document, string, integer → `None` | Calls `doc.add_heading`. |
| `add_paragraphs(*texts,doc=None)` | Strings plus optional Document → `None` | Appends normal paragraphs to explicit doc or global `CURRENT_DOC`; raises `ValueError` if neither exists. |
| `build_report()` | No explicit args → `None` | Creates a legacy DOCX with hard-coded content and placeholders; saves `project_report.docx`. It is not the Markdown report builder. |

These contracts describe actual operations; source functions do not declare Python type annotations.

## 13.12 Unused symbols and documentation caution

The source defines `rgb_to_bytes` and `int_to_rgb`, but actual header/payload conversion uses comprehensions and loops rather than those helpers. Prior synopsis and generated DOCX text refer to these functions as if part of the implementation flow; their existence is real, but their participation in encoding is not.
