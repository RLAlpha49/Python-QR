"""
This module generates QR codes with various options.
"""

import io
from typing import Optional

import qrcode
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def generate_qr(
    qr_data: str, is_dynamic: bool, qr_redirect_url: Optional[str], qr_img_format: str
) -> io.BytesIO:
    """
    Generates a QR code with the given data, dynamic flag, redirect URL, and image format.
    """
    if is_dynamic:
        qr_data = f"{qr_redirect_url}?data={qr_data}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format=qr_img_format)
    img_buffer.seek(0)
    return img_buffer


st.title("QR Code Generator")

data: str = st.text_input("Enter the data you want to encode into QR code")
dynamic: bool = st.checkbox("Make dynamic QR code")

redirect_url_placeholder: DeltaGenerator = st.empty()
REDIRECT_URL: Optional[str] = None
if dynamic:
    REDIRECT_URL = redirect_url_placeholder.text_input(
        "Enter the redirect URL for the dynamic QR code"
    )
else:
    redirect_url_placeholder.empty()

image_formats: list[str] = ["PNG", "JPEG", "TIFF", "BMP", "GIF", "PPM", "WEBP", "ICO"]
img_format: Optional[str] = None

if st.button("Generate QR Code"):
    if dynamic and not REDIRECT_URL:
        st.warning("Please enter a redirect URL for the dynamic QR code.")
    else:
        for img_format in image_formats:
            st.session_state[f"img_buffer_{img_format.lower()}"] = generate_qr(
                data, dynamic, REDIRECT_URL, img_format
            )

if "img_buffer_png" in st.session_state:
    st.image(st.session_state.img_buffer_png, use_column_width=True)

    img_format = st.selectbox("Select the image format for download:", image_formats)

    if img_format is not None:
        img_format_lower = img_format.lower()
        st.download_button(
            label=f"Download QR Code as {img_format}",
            data=st.session_state[f"img_buffer_{img_format_lower}"],
            file_name=f"qr_code.{img_format_lower}",
            mime=f"image/{img_format_lower}",
        )
