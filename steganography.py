"""LSB image encoding and decoding operations shared by the app interfaces."""

from PIL import Image


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
