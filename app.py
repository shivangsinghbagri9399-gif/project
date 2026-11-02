"""Streamlit web interface for the LSB steganography app."""

from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from steganography import (
    decrypt_message,
    encrypt_message,
    extract_message,
    hide_message,
    is_encrypted_message,
)


IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "gif", "webp", "tif", "tiff"]

st.set_page_config(page_title="LSB Steganography", page_icon="🖼️")
st.session_state.setdefault("encrypted_payload", None)
st.session_state.setdefault("decoded_message", None)
st.session_state.setdefault("decoded_message_encrypted", False)

st.title("LSB Steganography")
st.write("Hide a text message in an image or extract a message from an encoded image.")
st.info(
    "Password encryption is optional. Without it, the message is only hidden, "
    "not encrypted. Avoid uploading private images or sensitive text to a "
    "public deployment."
)

encode_tab, decode_tab = st.tabs(["Encode", "Decode"])

with encode_tab:
    st.subheader("Hide a message")
    encrypt_with_password = st.checkbox("Encrypt message with a password")
    if encrypt_with_password:
        st.caption(
            "Use a strong passphrase and keep it safe. Encryption adds data, "
            "so the image may need more capacity."
        )

    with st.form("encode_form"):
        cover_image = st.file_uploader(
            "Choose a cover image",
            type=IMAGE_TYPES,
            key="cover_image",
            max_upload_size=20,
        )
        secret_message = st.text_area("Message to hide")
        if encrypt_with_password:
            encryption_password = st.text_input(
                "Encryption password", type="password"
            )
            password_confirmation = st.text_input(
                "Confirm password", type="password"
            )
        else:
            encryption_password = ""
            password_confirmation = ""
        encode_submitted = st.form_submit_button("Encode image")

    if encode_submitted:
        if cover_image is None:
            st.error("Choose an image first.")
        elif not secret_message.strip():
            st.error("Enter a message to hide.")
        elif encrypt_with_password and not encryption_password:
            st.error("Enter a password or turn off password encryption.")
        elif encrypt_with_password and encryption_password != password_confirmation:
            st.error("The passwords do not match.")
        else:
            encoded_image = BytesIO()
            try:
                message_to_hide = (
                    encrypt_message(secret_message, encryption_password)
                    if encrypt_with_password
                    else secret_message
                )
                hide_message(
                    BytesIO(cover_image.getvalue()),
                    message_to_hide,
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
        st.session_state["encrypted_payload"] = None
        st.session_state["decoded_message"] = None
        st.session_state["decoded_message_encrypted"] = False
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
                if is_encrypted_message(message):
                    st.session_state["encrypted_payload"] = message
                else:
                    st.session_state["decoded_message"] = message

    if st.session_state["encrypted_payload"]:
        st.info("This image contains a password-encrypted message.")
        with st.form("decrypt_form"):
            decryption_password = st.text_input(
                "Enter the password", type="password"
            )
            decrypt_submitted = st.form_submit_button("Decrypt message")

        if decrypt_submitted:
            try:
                decoded_message = decrypt_message(
                    st.session_state["encrypted_payload"],
                    decryption_password,
                )
            except ValueError as error:
                st.error(str(error))
            else:
                st.session_state["decoded_message"] = decoded_message
                st.session_state["decoded_message_encrypted"] = True
                st.session_state["encrypted_payload"] = None
                st.rerun()

    if st.session_state["decoded_message"] is not None:
        if st.session_state["decoded_message_encrypted"]:
            st.success("Message decrypted successfully.")
        else:
            st.success("Message extracted.")
        st.text_area(
            "Hidden message",
            value=st.session_state["decoded_message"],
            height=160,
        )

st.caption(
    "Images are processed in memory by this app and are not intentionally saved. "
    "PNG is recommended; JPEG compression can destroy hidden data."
)
