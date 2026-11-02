
"""
Simple LSB steganography GUI (Tkinter)

Encode a text message into a PNG image, or decode a hidden message back.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar, IntVar

from PIL import Image, ImageTk
from steganography import (
    embed_bits_into_image,
    extract_bits_from_image,
    extract_message,
    hide_message,
    int_to_rgb,
    rgb_to_bytes,
)


# ----------------------------------------------------------------------
# Tkinter GUI
# ----------------------------------------------------------------------
class StegApp(tk.Tk):
    IMAGE_FILETYPES = [
        ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tif *.tiff *.jfif"),
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg *.jpeg *.jfif"),
        ("BMP files", "*.bmp"),
        ("GIF files", "*.gif"),
        ("WEBP files", "*.webp"),
        ("TIFF files", "*.tif *.tiff"),
        ("All files", "*.*"),
    ]

    def __init__(self):
        super().__init__()
        self.title("LSB Steganography Mini‑App")
        self.geometry("620x500")
        self.minsize(580, 420)
        self.resizable(True, True)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=8, font=("Helvetica", 10))
        self.style.configure("TLabel", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 11, "bold"))

        self._create_notebook()
        self._create_enc_tab()
        self._create_dec_tab()

    @staticmethod
    def _is_supported_image(path):
        if not path or not os.path.isfile(path):
            return False
        ext = os.path.splitext(path)[1].lower()
        supported_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff", ".jfif"}
        return ext in supported_exts

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_enc_tab(self):
        frame = ttk.Frame(self.notebook, padding=14)
        self.notebook.add(frame, text="Encode")

        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Select a cover image and hide a secret message.", style="Header.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 12)
        )

        # Image selector
        ttk.Label(frame, text="Cover Image (PNG):").grid(row=1, column=0, sticky="w", pady=5)
        self.enc_img_path = StringVar(value="")
        enc_entry = ttk.Entry(frame, textvariable=self.enc_img_path, width=42)
        enc_entry.grid(row=1, column=1, padx=(8, 8), sticky="ew")

        def browse_enc():
            path = filedialog.askopenfilename(
                title="Select photo to encode",
                filetypes=self.IMAGE_FILETYPES
            )
            if path:
                self.enc_img_path.set(path)

        ttk.Button(frame, text="Browse Photo", command=browse_enc).grid(row=1, column=2, padx=(0, 4), sticky="ew")

        # Message entry
        ttk.Label(frame, text="Secret message:").grid(row=2, column=0, sticky="w", pady=5)
        self.enc_msg = StringVar()
        ttk.Entry(frame, textvariable=self.enc_msg, width=42).grid(row=2, column=1, columnspan=2, padx=(8, 0), sticky="ew")

        # Encode button
        ttk.Button(frame, text="Encode → Save", command=self._encode).grid(
            row=3, column=0, columnspan=3, pady=(14, 8), sticky="ew"
        )

        # Feedback label
        self.enc_feedback = StringVar(value="Ready.")
        ttk.Label(frame, textvariable=self.enc_feedback, foreground="green").grid(
            row=4, column=0, columnspan=3, pady=2, sticky="w"
        )

    def _create_dec_tab(self):
        frame = ttk.Frame(self.notebook, padding=14)
        self.notebook.add(frame, text="Decode")

        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Select a stego image to extract hidden text.", style="Header.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 12)
        )

        # Image selector
        ttk.Label(frame, text="Stego Image (PNG):").grid(row=1, column=0, sticky="w", pady=5)
        self.dec_img_path = StringVar(value="")
        dec_entry = ttk.Entry(frame, textvariable=self.dec_img_path, width=42)
        dec_entry.grid(row=1, column=1, padx=(8, 8), sticky="ew")

        def browse_dec():
            path = filedialog.askopenfilename(
                title="Select photo to decode",
                filetypes=self.IMAGE_FILETYPES
            )
            if path:
                self.dec_img_path.set(path)

        ttk.Button(frame, text="Browse Photo", command=browse_dec).grid(row=1, column=2, padx=(0, 4), sticky="ew")

        # Decode button
        ttk.Button(frame, text="Decode → Show", command=self._decode).grid(
            row=2, column=0, columnspan=3, pady=(14, 8), sticky="ew"
        )

        # Feedback label
        self.dec_feedback = StringVar(value="Ready.")
        ttk.Label(frame, textvariable=self.dec_feedback, foreground="green").grid(
            row=3, column=0, columnspan=3, pady=2, sticky="w"
        )

        # Area to display extracted text
        self.decode_output = tk.Text(frame, height=8, width=58, state="disabled", wrap="word")
        self.decode_output.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")

    # ------------------------------------------------------------------
    # Encoding logic
    # ------------------------------------------------------------------
    def _encode(self):
        img_path = self.enc_img_path.get()
        message = self.enc_msg.get()
        if not self._is_supported_image(img_path):
            self.enc_feedback.set("❌ Choose a valid photo file first (.png, .jpg, .jpeg, .bmp, .gif, .webp, .tif, .tiff).")
            return
        if not message.strip():
            self.enc_feedback.set("❌ Enter a message to hide.")
            return

        try:
            out_path = img_path.rsplit(".", 1)[0] + "_encoded.png"
            hide_message(img_path, message, out_path)
            self.enc_feedback.set(f"✅ Saved encoded image: {os.path.basename(out_path)}")
        except Exception as e:
            self.enc_feedback.set(f"❌ Error: {str(e)}")

    # ------------------------------------------------------------------
    # Decoding logic
    # ------------------------------------------------------------------
    def _decode(self):
        img_path = self.dec_img_path.get()
        if not self._is_supported_image(img_path):
            self.dec_feedback.set("❌ Choose a valid photo file first (.png, .jpg, .jpeg, .bmp, .gif, .webp, .tif, .tiff).")
            return

        try:
            message = extract_message(img_path)
            # Show the decoded text
            self.decode_output.configure(state="normal")
            self.decode_output.delete("1.0", tk.END)
            self.decode_output.insert(tk.END, message)
            self.decode_output.configure(state="disabled")
            self.dec_feedback.set("✅ Message extracted.")
        except Exception as e:
            self.dec_feedback.set(f"❌ Extraction failed: {str(e)}")
            self.decode_output.configure(state="normal")
            self.decode_output.delete("1.0", tk.END)
            self.decode_output.insert(tk.END, f"[error] {e}")
            self.decode_output.configure(state="disabled")


if __name__ == "__main__":
    app = StegApp()
    app.mainloop()
