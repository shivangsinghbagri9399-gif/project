# Chapter 1 — Introduction

## 1.1 Background

Digital information is routinely transformed, stored, and transmitted as sequences of bits. Image steganography uses an image as a carrier and changes selected image samples to encode another data stream. This project demonstrates one direct spatial-domain method: replace the low-order bit of each of the three RGB channels with one payload bit. The project is small enough to inspect end-to-end: [steg_app.py](../../steg_app.py) contains both the GUI and the image transformations.

## 1.2 Information security

Information security concerns protection against unauthorized disclosure, alteration, and disruption. This implementation is relevant to confidentiality as a teaching illustration, but its bit replacement does not itself establish access control, encryption, authentication, or integrity. The distinction matters because successful recovery by the intended user does not demonstrate security against an adversary.

## 1.3 Confidentiality

Confidentiality means preventing unauthorized parties from learning protected content. In the present program, the message remains in its original representation apart from UTF-8 encoding. No key or cipher is used. A reader who knows or discovers the fixed format can decode the message, so the application does not provide cryptographic confidentiality.

## 1.4 Data hiding

Data hiding places information inside a host object. In this application, the host is a decoded image represented as RGB tuples and the payload is text converted to bytes. The operation changes channel parity, not the file’s visible high-level structure.

## 1.5 Steganography

Steganography aims to conceal the existence of communication; NIST defines it as communication that hides the existence of the communication [1]. This program is an elementary example: there is no marker in the file format that tells an image viewer the payload exists, but the format is also fixed and unkeyed, making extraction straightforward for an informed observer.

## 1.6 Historical development

Concealment of messages predates digital computing, but this report does not attempt an unsupported historical survey. The implementation is specifically a modern spatial-domain, digital-image demonstration. A detailed historical chronology is not available in the project sources.

## 1.7 Digital steganography

Digital steganography changes or augments a digital carrier. Its effectiveness depends not only on recovering a payload but also on whether the changes remain inconspicuous and survive expected handling. The application implements direct sample modification only; it does not evaluate these properties experimentally.

## 1.8 Image steganography

An image supplies many sample values that can carry bits. Here Pillow decodes the selected file and the application reduces it to RGB. The pixel values—not compressed file bytes or metadata—are the embedding domain.

## 1.9 Spatial-domain steganography

Spatial-domain methods modify image samples directly. This application replaces sample LSBs, requiring only bitwise masking and insertion. It does not use a frequency transform, quantization coefficients, or adaptive content analysis.

## 1.10 Transform-domain steganography

Transform-domain schemes embed information in transformed image representations, such as frequency coefficients, and can offer different robustness/quality trade-offs. No transform-domain operation exists in the current source; this discussion is background only, not a project feature.

## 1.11 LSB steganography

For an 8-bit channel value `C`, the code applies `(C & 0xFE) | b`, where `b` is 0 or 1. This clears the original low bit and sets it to the payload bit. A channel changes by 0 or 1. The method is reversible only while the encoded samples survive unchanged and the decoder follows the same traversal and framing rules.

## 1.12 RGB representation

After `Image.open(...).convert("RGB")`, each pixel has three 8-bit components `(R,G,B)`. The algorithm's storage capacity is three bits per pixel. An alpha component, if present in the source, is discarded by RGB conversion; it is not used to store data.

## 1.13 Pixel structure

Pillow yields image pixels in row-major order when iterating `getdata()`. For each pixel the application processes red, green, then blue. This deterministic ordering is part of the informal file format: changing either order makes existing payloads undecodable.

## 1.14 Binary representation

Each UTF-8 byte has eight bits. Both the 32-bit header and each message byte are emitted most-significant bit first. The decoder reconstructs integers by shifting the accumulated value left and OR-ing the next bit. This is big-endian ordering at the bit-stream level; no separate byte-order field is stored.

## 1.15 PNG

PNG is a lossless raster-image format. Its decoded sample values can preserve embedded RGB LSBs through a PNG save/load cycle. The application always writes its output to a `.png` path; it accepts other image extensions at input, and Pillow then decodes and converts their samples. Merely changing the extension of an image does not make a lossy source suitable.

## 1.16 Lossless compression

Lossless compression reproduces the input samples exactly after decompression. That property is useful to this algorithm because the decoder depends on exact low bits. PNG’s specification describes a lossless image format [4]. It does not make the payload robust to later resizing, filtering, color changes, or lossy re-encoding.

## 1.17 Steganography versus cryptography

Steganography attempts to hide that a message exists; cryptography transforms message content under a cryptographic scheme. The app performs only the former. It contains no encryption library, password, or key management. A stronger design would encrypt and authenticate the payload before embedding it, but those mechanisms are not implemented here.

## 1.18 Motivation

The implementation joins text encoding, image processing, bitwise operations, GUI events, and file I/O in a compact example. This makes the code useful for demonstrating data representation and the limits of naive hiding without introducing a database or server.

## 1.19 Research gap

The project is not a research evaluation of competing steganographic methods. It does not quantify detection rates, image quality, payload efficiency, or robustness. Its appropriate contribution is implementation transparency and a runnable baseline from which controlled experiments could be designed.

## 1.20 Problem context

The immediate engineering problem is to encode a variable-length text message into a finite sequence of RGB channel LSBs and later recover exactly the declared number of bits. Correctness requires consistent UTF-8 conversion, a length prefix, matching traversal order, and a capacity check.

## 1.21 Proposed system

The system has one process and one source module: Tkinter gathers paths and text; `hide_message` or `extract_message` performs the pixel operation using Pillow; local files provide input and output. There is no service layer, database, or formal multi-module package.

## 1.22 Contribution of the project

The demonstrated contribution is a simple GUI and reversible sequential LSB encoding/decoding implementation with a 32-bit payload-length field, basic capacity validation, and four executable test functions. No novel algorithm or security guarantee is claimed.

## 1.23 Educational and technical significance

The code makes the relationship between a text byte and three RGB channel samples observable. It also exposes practical concerns—payload length, channel order, capacity, lossy transformations, tolerant decoding, and false positives—that are valuable in introductory security and image-processing study.

## 1.24 Limitations

The implementation is sequential, keyless, unencrypted, unauthenticated, and not robust to sample-changing operations. It has no format magic or checksum, and it ignores invalid UTF-8 bytes on extraction. The UI accepts multiple extensions despite PNG-focused labels and documentation. Its tests do not exercise GUI behavior.

## 1.25 Chapter summary

This project is best characterized as a local educational demonstration of spatial RGB-LSB data hiding. PNG output supports exact sample persistence, but neither PNG nor imperceptible-looking pixel changes provide security. The following chapters describe the implementation boundary, formal data model, and evidence precisely.

**Implementation trace:** [steg_app.py](../../steg_app.py#L1), [requirements.txt](../../requirements.txt), [test_steg.py](../../test_steg.py).
