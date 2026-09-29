# Chapter 10 — Data Flow Diagram

The diagrams show local file and in-memory data flows. No database is involved.

## 10.1 Context DFD

```mermaid
flowchart LR
  U[External entity: User]
  APP((LSB Steganography Mini-App))
  FS[(Local file system)]
  U -->|Image path, message, encode/decode action| APP
  APP -->|Status, recovered text| U
  FS -->|Selected source/stego image bytes| APP
  APP -->|Encoded PNG file| FS
```

**Figure 3.** Context-level view. The file system is shown as a local storage boundary, not a database.

## 10.2 Level-0 DFD

```mermaid
flowchart LR
  U[User]
  FS[(Local file system)]
  P1((1. Validate selection))
  P2((2. Encode message))
  P3((3. Decode message))
  D1[(In-memory decoded RGB samples)]

  U -->|Path, message, requested action| P1
  P1 -->|Accepted path and operation| P2
  P1 -->|Accepted path and operation| P3
  FS -->|Input image file| P2
  FS -->|Stego image file| P3
  P2 -->|Decode and RGB samples| D1
  U -->|Message text| P2
  P2 -->|Encoded image samples| FS
  P3 -->|RGB samples| D1
  P3 -->|Recovered text/status| U
  P1 -->|Validation feedback| U
```

**Figure 4.** Level-0 DFD; the in-memory sample store is transient process memory, not persistent storage.

## 10.3 Level-1 DFD

### Encoding path

```mermaid
flowchart LR
  U[User] -->|Path and text| V((1.1 Validate path and nonblank text))
  V -->|Path| O((1.2 Pillow open and convert RGB))
  FS[(Local file system)] -->|Input image| O
  O -->|W × H RGB pixels| C((1.3 Compute capacity))
  U -->|Text| B((1.4 UTF-8 encode and form bits))
  B -->|32-bit bit-length header + payload| E((1.5 Replace RGB LSBs))
  C -->|Capacity decision| E
  O -->|RGB samples| E
  E -->|Modified image| S((1.6 Save PNG))
  S -->|New encoded image| FS
  E -->|Success/error status| U
```

### Decoding path

```mermaid
flowchart LR
  U[User] -->|Stego image path| O((2.1 Pillow open and convert RGB))
  FS[(Local file system)] -->|Selected image| O
  O -->|RGB pixels| H((2.2 Read first 32 LSBs))
  H -->|Length in bits| V((2.3 Validate byte alignment and capacity))
  O -->|Remaining RGB LSB stream| X((2.4 Read declared payload))
  V -->|Valid length| X
  X -->|Payload bits| R((2.5 Rebuild bytes))
  R -->|Bytes| T((2.6 UTF-8 decode, ignore errors))
  T -->|Recovered text/status| U
```

**Figure 5.** Level-1 operations. The decoder has no signature check; a non-stego image can contain a plausible header by chance.

## Data-flow notes

- Encode reads an image and text; it writes a new image.
- Decode reads a selected image and returns text only to the GUI.
- Status/errors flow to the user interface.
- No persistent message history, configuration store, database, or remote endpoint is present.
