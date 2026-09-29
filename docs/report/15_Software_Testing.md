# Chapter 15 — Software Testing

## 15.1 Methodology

The existing test harness is a direct executable Python script. It creates RGB images with Pillow, writes them under `tempfile.TemporaryDirectory`, invokes the core helpers, and returns booleans. The script-level runner catches exceptions, counts pass/fail cases, prints totals, and exits 0 only if all four tests pass.

## 15.2 Unit and integration testing

The tests functionally exercise `hide_message` and `extract_message` together, so the round trips are small integration tests of image conversion, embedding, saving, re-opening, extraction, and text decoding. There are no isolated unit tests for `embed_bits_into_image`, header encoding, or `extract_bits_from_image`.

## 15.3 Test environment and actual run

Observed environment: Python 3.14.4, Pillow 12.3.0, macOS workspace. Command:

```bash
./.venv/bin/python test_steg.py
```

Observed final output:

```text
Test Results: 4 passed, 0 failed
```

No separate coverage tool or GUI environment test was run.

## 15.4 Test case inventory

| ID | Test function | Input and setup | Expected behavior / assertion | Actual result |
|---|---|---|---|---|
| T01 | `test_encode_decode` | Generated 200×200 solid RGB image; ASCII phrase | Encoded output exists and decoded string equals original | PASS |
| T02 | `test_capacity_limits` | Generated 10×10 RGB image; 100 ASCII `A` characters | `hide_message` raises `ValueError` because 800 bits exceed 268 payload bits | PASS |
| T03 | `test_utf8_support` | Generated 200×200 RGB image; mixed Latin, CJK, emoji, Japanese text | Exact decoded string equality | PASS |
| T04a | `test_multiple_images` | 50×50 RGB image; `"Test message"` | Encode/decode equality | PASS |
| T04b | `test_multiple_images` | 100×100 RGB image; same text | Encode/decode equality | PASS |
| T04c | `test_multiple_images` | 500×500 RGB image; same text | Encode/decode equality | PASS |

The script has four test functions, containing seven dimension/outcome subchecks when the three cases in T04 are counted individually.

## 15.5 Boundary, negative, and capacity coverage

The test suite includes one oversized-message rejection but does not test exact maximum capacity, one byte over capacity, an image below 32 channel bits, a 32-bit header with zero payload, malformed header alignment, or header length beyond capacity. A valid minimal RGB image needs at least 11 pixels to provide 33 channel slots and a whole byte after the 32-bit header.

## 15.6 UTF-8 coverage

One non-ASCII string is tested and round-tripped exactly. The suite does not test all Unicode scalar values, embedded NUL, combining sequences, very long multi-byte strings, or malformed byte sequences. The decoder’s `errors="ignore"` behavior is not tested.

## 15.7 Image and GUI coverage

Only generated RGB PNG inputs are used. No grayscale, RGBA, palette, animated GIF, TIFF, WebP, JPEG, or corrupted image test exists. `StegApp` is never instantiated, so file dialogs, widget state, path allowlisting, status text, and GUI error output remain unverified.

## 15.8 Test limitations

- Tests are custom print/boolean functions rather than pytest/unittest tests.
- Assertions are implemented as conditional branches, not framework assertion reporting.
- `test_multiple_images` catches broad `Exception`.
- No test coverage percentage exists.
- No performance or image-quality measurement exists.
- The zero-byte sample placeholder is not used by tests.

## 15.9 Testing conclusion

Evidence supports basic functionality for generated RGB PNGs, one Unicode sample, one oversize rejection, and three dimensions. It does not support claims about GUI quality, general image-mode support, invalid-input completeness, security, perceptual quality, robustness, or performance.
