# Chapter 2 — Objectives

The table distinguishes the intended purpose from what can be verified in the current code. “Evidence” refers to implementation or test coverage, not a claim that every desirable property has been proven.

| Objective | Purpose and rationale | Implementation and measurable evidence |
|---|---|---|
| 2.1 Primary objective | Demonstrate hiding and recovery of text in an image. | `hide_message` and `extract_message` provide the operations; the round-trip test checks exact ASCII recovery. |
| 2.2 Research objective | Provide a transparent baseline for discussing LSB trade-offs. | The deterministic algorithm can be inspected; no comparative or statistical experiment is implemented. |
| 2.3 Technical objectives | Combine Python, Pillow, and Tkinter. | `steg_app.py` imports these; `requirements.txt` declares `pillow>=10.0.0`. |
| 2.4 Functional objectives | Encode, save, select, and display recovered text. | Encode/Decode tabs call the helpers; four test functions exercise the non-GUI encoding path. |
| 2.5 Algorithmic objectives | Frame, embed, extract, and reconstruct payload bits. | A 32-bit payload-length-in-bits header and MSB-first RGB traversal are implemented. |
| 2.6 GUI objectives | Offer a simple event-driven desktop interaction. | `StegApp` creates two tabs, file dialogs, a single-line message entry, feedback labels, and decoded output. GUI execution itself was not tested. |
| 2.7 Data-integrity objective | Recover the original text when image samples are preserved. | Exact equality is asserted in round-trip tests. There is no cryptographic integrity check; “integrity” here means functional round-trip correctness only. |
| 2.8 Validation objective | Reject invalid selections and payloads that exceed capacity. | The UI checks file existence/extension and non-whitespace text; the encoder checks bit capacity; decoder checks header alignment and capacity. |
| 2.9 Testing objective | Check normal, Unicode, size, and capacity cases. | `test_steg.py` includes these four categories. No pytest/unittest framework, UI tests, or coverage report is present. |
| 2.10 Security-analysis objective | State what data hiding does and does not protect. | The report documents key absence, detectability, integrity, and transformations; the application has no security subsystem. |
| 2.11 Educational objective | Make data representation and LSB behavior inspectable. | Small helpers and direct Pillow operations expose the mechanics. No measured learning outcome is available. |

The tested result is limited to the specific inputs in [test_steg.py](../../test_steg.py); see [Chapter 15](./15_Software_Testing.md). No assertion measures invisibility, robustness, or production suitability.
