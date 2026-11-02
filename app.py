"""Streamlit web interface for the LSB steganography app."""

from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from steganography import extract_message, hide_message


IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "gif", "webp", "tif", "tiff"]

st.set_page_config(page_title="LSB Steganography", page_icon="🖼️")
st.title("LSB Steganography")
st.write("Hide a text message in an image or extract a message from an encoded image.")
st.info(
    "This educational tool does not encrypt messages. Avoid uploading private "
    "images or sensitive text to a public deployment."
)

encode_tab, decode_tab = st.tabs(["Encode", "Decode"])

with encode_tab:
    st.subheader("Hide a message")
    with st.form("encode_form"):
        cover_image = st.file_uploader(
            "Choose a cover image",
            type=IMAGE_TYPES,
            key="cover_image",
            max_upload_size=20,
        )
        secret_message = st.text_area("Message to hide")
        encode_submitted = st.form_submit_button("Encode image")

    if encode_submitted:
        if cover_image is None:
            st.error("Choose an image first.")
        elif not secret_message.strip():
            st.error("Enter a message to hide.")
        else:
            encoded_image = BytesIO()
            try:
                hide_message(
                    BytesIO(cover_image.getvalue()),
                    secret_message,
                    encoded_image,
                )
            except (
                UnidentifiedImageError,
                OSError,
                ValueError,
                Image.DecompressionBombError,
            ) as error:
                st.error(f"Could not encode the image: {error}")
            else:
                base_name = (
                    cover_image.name.rsplit(".", 1)[0]
                    if "." in cover_image.name
                    else cover_image.name
                )
                output_name = f"{base_name}_encoded.png"
                st.success("Message encoded successfully.")
                st.download_button(
                    "Download encoded PNG",
                    data=encoded_image.getvalue(),
                    file_name=output_name,
                    mime="image/png",
                )

with decode_tab:
    st.subheader("Extract a hidden message")
    with st.form("decode_form"):
        stego_image = st.file_uploader(
            "Choose an encoded image",
            type=IMAGE_TYPES,
            key="stego_image",
            max_upload_size=20,
        )
        decode_submitted = st.form_submit_button("Decode image")

    if decode_submitted:
        if stego_image is None:
            st.error("Choose an image first.")
        else:
            try:
                message = extract_message(BytesIO(stego_image.getvalue()))
            except (
                UnidentifiedImageError,
                OSError,
                ValueError,
                Image.DecompressionBombError,
            ) as error:
                st.error(f"Could not decode the image: {error}")
            else:
                st.success("Message extracted.")
                st.text_area("Hidden message", value=message, height=160)

st.caption(
    "Images are processed in memory by this app and are not intentionally saved. "
    "PNG is recommended; JPEG compression can destroy hidden data."
)
