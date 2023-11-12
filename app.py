import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

# Function to generate download link for binary files
def get_binary_file_downloader_html(bin_file, file_label="Download"):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

def compress_image(original_image, compression_level):
    if compression_level == "High":
        quality = 80
    elif compression_level == "Medium":
        quality = 60
    elif compression_level == "Low":
        quality = 40
    else:
        raise ValueError("Invalid compression level")

    output_buffer = BytesIO()
    original_image.save(output_buffer, format="JPEG", quality=quality)
    compressed_image = Image.open(output_buffer)
    return compressed_image

st.title("Image Compressor")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display original image
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    # Compression options
    compression_option = st.radio("Select Compression Level:", ("High", "Medium", "Low"))

    # Compress image
    compressed_image = compress_image(original_image, compression_option)

    # Display compressed image
    st.image(compressed_image, caption=f"Compressed Image ({compression_option} Compression)", use_column_width=True)

    # Download compressed image
    download_button = st.button("Generate Download Link for Compressed Image")
    if download_button:
        target_filename = os.path.splitext(uploaded_file.name)[0] + f"_compressed_{compression_option.lower()}.jpg"
        compressed_image.save(target_filename)
        st.success(f"Compressed image downloaded as {target_filename}")

        # Generate download link
        st.markdown(get_binary_file_downloader_html(target_filename), unsafe_allow_html=True)

        # Balloon animation
        if st.button("NK21❤️"):
            st.balloons()

# Developer information
st.sidebar.title("Dev")
st.sidebar.markdown(
    """
    **Developer:** NK21
    https://t.me/technicalsagar7
    """
)
