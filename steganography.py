"""LSB image encoding and decoding operations shared by the app interfaces."""

import base64
import binascii
import os

from PIL import Image

ENCRYPTED_MESSAGE_PREFIX = "LSB-ENC:v1:"
KEY_ENCRYPTED_MESSAGE_PREFIX = "LSB-KEY:v1:"
PASSWORD_KDF_ITERATIONS = 1_200_000


def is_encrypted_message(message):
    """Return whether a decoded payload uses this app's encrypted format."""
    return is_password_encrypted_message(message) or is_key_encrypted_message(message)


def is_password_encrypted_message(message):
    """Return whether a decoded payload uses password-based encryption."""
    return message.startswith(ENCRYPTED_MESSAGE_PREFIX)


def is_key_encrypted_message(message):
    """Return whether a decoded payload uses a separate generated key."""
    return message.startswith(KEY_ENCRYPTED_MESSAGE_PREFIX)


def _derive_encryption_key(password, salt):
    """Derive a Fernet key from a password and per-message random salt."""
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PASSWORD_KDF_ITERATIONS,
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8"))))


def encrypt_message(message, password):
    """Encrypt UTF-8 text and return an ASCII envelope safe to hide in an image."""
    if not password:
        raise ValueError("Enter a password to encrypt the message.")

    salt = os.urandom(16)
    encrypted = _derive_encryption_key(password, salt).encrypt(
        message.encode("utf-8")
    )
    encoded_salt = base64.urlsafe_b64encode(salt).decode("ascii")
    return f"{ENCRYPTED_MESSAGE_PREFIX}{encoded_salt}:{encrypted.decode('ascii')}"


def encrypt_message_with_key(message):
    """Encrypt text with a random key returned for separate safekeeping."""
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    encrypted = Fernet(key).encrypt(message.encode("utf-8"))
    envelope = f"{KEY_ENCRYPTED_MESSAGE_PREFIX}{encrypted.decode('ascii')}"
    return envelope, key


def decrypt_message(envelope, password):
    """Authenticate and decrypt an encrypted message envelope."""
    from cryptography.fernet import InvalidToken

    if not password:
        raise ValueError("Enter the password used to encrypt this message.")
    if not is_encrypted_message(envelope):
        raise ValueError("This image does not contain a password-encrypted message.")

    try:
        encoded_salt, token = envelope[len(ENCRYPTED_MESSAGE_PREFIX):].split(":", 1)
        salt = base64.b64decode(encoded_salt, altchars=b"-_", validate=True)
        if len(salt) != 16:
            raise ValueError("Invalid encryption metadata.")
        plaintext = _derive_encryption_key(password, salt).decrypt(
            token.encode("ascii")
        )
        return plaintext.decode("utf-8")
    except (InvalidToken, binascii.Error, UnicodeError, ValueError):
        raise ValueError(
            "Wrong password or encrypted message is damaged."
        ) from None


def decrypt_message_with_key(envelope, key):
    """Authenticate and decrypt a generated-key message using its key file."""
    from cryptography.fernet import Fernet, InvalidToken

    if not is_key_encrypted_message(envelope):
        raise ValueError("This image does not use a generated decryption key.")

    try:
        token = envelope[len(KEY_ENCRYPTED_MESSAGE_PREFIX):].encode("ascii")
        plaintext = Fernet(key.strip()).decrypt(token)
        return plaintext.decode("utf-8")
    except (InvalidToken, TypeError, UnicodeError, ValueError):
        raise ValueError(
            "Wrong key or encrypted message is damaged."
        ) from None


def rgb_to_bytes(r, g, b):
    """Pack three 8-bit channels into a single 24-bit integer."""
    return (r << 16) | (g << 8) | b


def int_to_rgb(value):
    """Unpack a 24-bit integer back to (R, G, B)."""
    return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)


def extract_bits_from_image(image):
    """Yield LSBs from each channel of each pixel (row-major order)."""
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


def embed_bits_into_image(image, bits, max_bits):
    """Replace pixel-channel LSBs with `bits`, up to `max_bits`."""
    if len(bits) > max_bits:
        raise ValueError(
            f"Message too long for this image (needs {len(bits)} bits, "
            f"max {max_bits} available)."
        )

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

    raw = list(image.getdata())
    new_pixels.extend(raw[len(new_pixels):])

    new_img = Image.new(image.mode, image.size)
    new_img.putdata(new_pixels)
    return new_img


def hide_message(image_path, message, output_path):
    """Encode `message` into an image and save the result as PNG."""
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

    stego_img = embed_bits_into_image(img, length_bits + msg_bits, capacity_bits)
    stego_img.save(output_path, format="PNG")
    return stego_img


def extract_message(stego_path):
    """Decode hidden text from an image."""
    img = Image.open(stego_path).convert("RGB")
    width, height = img.size

    capacity_bits = width * height * 3
    if capacity_bits < 32:
        raise ValueError("Image is too small to contain a hidden message.")

    bit_iter = extract_bits_from_image(img)
    message_len_bits = 0
    for _ in range(32):
        message_len_bits = (message_len_bits << 1) | next(bit_iter, 0)

    if message_len_bits % 8:
        raise ValueError("The encoded message length is invalid.")
    if message_len_bits > capacity_bits - 32:
        raise ValueError("The image does not contain a valid hidden message.")

    bit_iter = extract_bits_from_image(img)
    for _ in range(32):
        next(bit_iter, 0)

    message_bytes = bytearray()
    for _ in range(message_len_bits // 8):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | next(bit_iter, 0)
        message_bytes.append(byte)

    return bytes(message_bytes).decode("utf-8", errors="ignore")
