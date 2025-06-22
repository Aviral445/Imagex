import streamlit as st
from stegano import lsb
from PIL import Image
import io

st.set_page_config(page_title="Stego App by Demigod", layout="centered")

st.title("🕵️‍♂️ Steganography Tool by Demigod")
st.caption("Hide secret messages in images or extract them.")

st.sidebar.title("Choose Mode")
mode = st.sidebar.radio("Select an option:", ["Encode Message", "Decode Message"])

# ---------- Encode Mode ----------
if mode == "Encode Message":
    st.header("🔐 Hide a Secret Message in an Image")

    uploaded_image = st.file_uploader("Upload a PNG image", type=["png"])
    message = st.text_area("Enter the secret message:")

    if uploaded_image and message:
        image = Image.open(uploaded_image)

        # Save temp image to encode message
        temp_path = "temp_input_image.png"
        image.save(temp_path)

        # Encode
        stego_image = lsb.hide(temp_path, message)

        # Convert to downloadable buffer
        buf = io.BytesIO()
        stego_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(stego_image, caption="Stego Image", use_column_width=True)
        st.download_button("⬇️ Download Stego Image", byte_im, "stego_image.png", "image/png")

# ---------- Decode Mode ----------
elif mode == "Decode Message":
    st.header("🧠 Extract a Secret Message from an Image")

    uploaded_stego = st.file_uploader("Upload a stego PNG image", type=["png"])

    if uploaded_stego:
        # Save and decode
        stego_image = Image.open(uploaded_stego)
        stego_image.save("temp_stego.png")
        hidden_message = lsb.reveal("temp_stego.png")

        if hidden_message:
            st.success("✅ Hidden message found!")
            st.code(hidden_message)
        else:
            st.error("❌ No hidden message found in the image.")
