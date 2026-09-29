# Chapter 4 — Problem Definition

## 4.1 Problem background

An image has a finite number of decoded color samples. A text payload has a variable number of bytes. A reversible hiding operation must map payload bits to sample bits, preserve their order, encode the payload boundary, and reject data that does not fit.

## 4.2 Communication privacy

Privacy may concern either message content or the fact that a message is being communicated. The program addresses only a basic form of the second concern by placing bits inside image samples; it does not protect content if the hidden payload is extracted.

## 4.3 Visibility of communication

The output remains a normal image file, but its RGB least significant bits carry a regular sequential bitstream. File appearance alone does not establish that the image is statistically indistinguishable from an ordinary cover image. No such experiment was conducted.

## 4.4 Conventional encryption

Encryption protects content by transforming it under a cryptographic algorithm and key. No cryptographic transformation occurs in this application. The message is directly recoverable in its UTF-8 representation by following the fixed header and traversal.

## 4.5 Steganographic approach

The implemented approach selects every RGB sample in raster order and replaces its lowest bit until the header plus message has been written. There is no random selection, key, adaptive location choice, or payload encoding beyond UTF-8.

## 4.6 Technical problem

Given an RGB image of width `W` and height `H`, and a message `m`, encode enough information in the image so that a matching decoder returns `m`, provided the sample values remain unchanged and the payload fits.

## 4.7 Data representation problem

The Python string must become bytes using UTF-8, and each byte must become eight ordered bits. The implementation uses the most-significant bit first for each byte. The header stores payload length in bits, also most-significant bit first.

## 4.8 Capacity problem

There are `3WH` RGB channel positions, one bit per position. The first 32 positions carry the length field, leaving `3WH - 32` bits for the payload. A payload of `M` UTF-8 bytes fits when `8M <= 3WH - 32`. If the expression on the right is negative, no payload, not even a complete header, fits.

## 4.9 Extraction problem

The decoder must read the same R-G-B order, reconstruct the fixed 32-bit bit count, verify that it is byte-aligned and within capacity, then reconstruct exactly that many payload bits. The implementation has no magic value to establish that an arbitrary image was produced by this encoder.

## 4.10 Validation problem

Validation exists at two levels. The GUI checks a nonempty existing path with an allowed suffix and rejects whitespace-only input. The core encoder checks payload capacity. The decoder checks minimum header capacity, bit-count divisibility by eight, and maximum capacity. It does not validate content authenticity or a payload signature.

## 4.11 Reliability problem

Exact recovery depends on sample preservation and matching decoder assumptions. PNG output supports lossless storage, but external transformations can alter LSBs. No redundancy or error correction repairs changed bits.

## 4.12 Security problem

The same deterministic format that makes the teaching implementation understandable also makes extraction simple. An observer can inspect channel LSBs, read a fixed 32-bit header, and recover bytes. There is no secret key, encryption, authentication, or defense against statistical detection.

## 4.13 Formal problem statement

Let `I` be an RGB image with `W × H` pixels and let `m` be a Unicode string. Let `B = UTF8(m)` and `L = 8|B|`. For `L <= 3WH - 32`, construct a channel-bit sequence consisting of `L` encoded as an unsigned 32-bit MSB-first integer followed by the MSB-first bits of `B`. Replace the LSBs of the first `32 + L` RGB channel samples in raster order with this sequence. Given the resulting image and unchanged samples, recover `L`, reconstruct `B`, and return the UTF-8 decoded text. The program does not define behavior for adversarial authenticity or error recovery.

## 4.14 Proposed approach

The implementation uses Pillow for image decoding/conversion and output, Tkinter for interaction, and Python integer/byte operations for bit framing. The formal algorithm and actual code are described in [Chapter 7](./07_Technical_Overview.md) and [Chapter 13](./13_Coding_Detailed_Explanation.md).

## Threat model

| Actor capability | Threat | Impact in this implementation | Existing mitigation / residual gap |
|---|---|---|---|
| Obtain the stego image | Read RGB values and apply known fixed extraction | Payload can be recovered without a key | None; no encryption or key |
| Inspect pixel values/statistics | Detect non-natural LSB patterns or infer embedding | Disclosure of hidden communication | No keyed/adaptive embedding or detection evaluation |
| Modify image samples | Change, clear, or randomize LSBs | Payload corruption or arbitrary output | Capacity checks only; no checksum, MAC, or correction |
| Re-encode or resize image | Trigger quantization/interpolation or sample remapping | Header/payload becomes invalid or changes | Recommend preserving PNG samples; no transformation resistance |
| Supply malformed image file | Exercise Pillow decoding and GUI exception paths | Operation failure; resource consumption depends on file | Pillow parsing errors reach UI catch block; no explicit file-size/pixel limit |
| Choose a non-stego image | Interpret initial LSBs as a length | Error or false-looking text if header is plausible | Plausibility checks only; no magic identifier |

This is an educational threat model, not a penetration test. The application is not designed to defend against these actors.
