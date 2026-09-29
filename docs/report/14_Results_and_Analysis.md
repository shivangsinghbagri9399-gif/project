# Chapter 14 — Results and Analysis

## 14.1 Evidence basis

Results below are separated into measured checks, direct source properties, and unmeasured expectations. The test command executed was `./.venv/bin/python test_steg.py` using the configured Python 3.14.4 environment and Pillow 12.3.0.

## 14.2 Functional result

The script returned exit status 0 and printed **4 passed, 0 failed**. This demonstrates that the four functions completed as expected for their specific generated test images. It does not establish GUI correctness or general reliability.

## 14.3 Encoding and decoding result

The ASCII test wrote an output image and recovered `"Hello, this is a secret message!"` exactly. The test only checks output existence and equality after extraction.

## 14.4 Round-trip and UTF-8 result

The Unicode test’s string (`Hello 世界! 🌍 こんにちは`) was recovered exactly in the observed run. This establishes UTF-8 round-trip behavior for that test string and image, not all Unicode text or all payload lengths.

## 14.5 Capacity result

A 10×10 RGB image provides 300 channel bits; after the 32-bit header, 268 bits remain, equivalent to 33 whole payload bytes (4 bits unused). The test message contains 100 ASCII bytes / 800 bits and was rejected with `ValueError("Image is too small to hold this message.")`.

## 14.6 Multiple image sizes

The test script reported successful short-message round trips at 50×50, 100×100, and 500×500. These are functional checks, not performance measurements.

## 14.7 GUI and image result

The GUI was not run or automated. The output image’s visual similarity was not assessed by a human protocol or image metric. The bundled `project-diagram.png` is a 1600×980 RGB diagram artifact; `samples/placeholder.png` is empty and not a valid image.

## 14.8 Error handling result

The oversized-payload `ValueError` path is tested. The suite does not test invalid extensions, nonexistent files, malformed image bytes, invalid length headers, non-byte-aligned headers, save failures, or UI feedback. Decoder validation branches are source-inspected, not runtime-tested here.

## 14.9 Performance and complexity

No timing or memory benchmark is included. Derivation from code: with `P=WH` and `M` UTF-8 bytes, encoding and decoding require O(P+M) time. Encoding allocates O(P+M) additional Python objects; decoding allocates O(P+M) additional objects. Actual constant factors may be substantial because each bit is stored as a Python list element and pixels are materialized into tuples/lists.

## 14.10 Capacity analysis

For dimensions `W×H`:

```text
total channel slots       N = 3WH bits
header                     = 32 bits
usable payload             = N - 32 bits, when N >= 32
whole payload bytes        = floor((3WH - 32) / 8)
fit condition for M bytes  = 8M <= 3WH - 32
```

| Image size | Total slots | Payload bits after header | Maximum whole payload bytes | Approximate ASCII characters |
|---:|---:|---:|---:|---:|
| 10×10 | 300 | 268 | 33 | 33 |
| 100×100 | 30,000 | 29,968 | 3,746 | 3,746 |
| 500×500 | 750,000 | 749,968 | 93,746 | 93,746 |
| 1000×1000 | 3,000,000 | 2,999,968 | 374,996 | 374,996 |

ASCII characters are one byte each; non-ASCII UTF-8 text may have fewer characters than byte capacity. For 100×100, the README claims approximately 373 characters, but that arithmetic does not match the implementation; correct capacity under the source algorithm is 3,746 bytes. This report’s example derives directly from source formula.

## 14.11 Security and steganographic quality

Capacity, imperceptibility, robustness, and detectability trade off. This implementation uses all three RGB channels for each payload bit and deterministic sequential selection. For each embedded bit, a channel is changed only when its original parity differs; for uniformly distributed payload bits, roughly half the touched channels would be expected to change, but the project has not measured the actual ratio on representative images. The code does not calculate PSNR, SSIM, histogram changes, or steganalysis detection rates.

Increasing payload increases the number of channel samples whose LSBs are overwritten and can alter local or global LSB statistics. No claim that these changes are visually imperceptible or statistically undetectable is substantiated by experiment. The method is not robust to operations that alter samples.

## 14.12 Reliability and limitations

The exact same path works for tested PNG files. There is no error correction. A corrupted header may raise validation errors, while a corrupted payload can be silently altered by the UTF-8 `ignore` policy. No payload authenticity is provided.

## Results table

| Claim | Evidence class | Result |
|---|---|---|
| Normal round trip works | Executed test | Pass |
| Oversized input rejected | Executed test | Pass |
| Test Unicode sample round trips | Executed test | Pass |
| Three tested dimensions support short payload | Executed test | Pass |
| GUI works on target display | Not executed | Requires verification |
| Image is visually imperceptible | Not measured | Requires experimental verification |
| Robust after JPEG/resizing/filtering | Not tested; not expected from algorithm | Not implemented |
| Runtime is acceptable for large images | Not benchmarked | Requires measurement |
