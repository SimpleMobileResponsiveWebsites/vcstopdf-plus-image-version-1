import streamlit as st
from PIL import Image

def main():
    st.title("Image Upload Application")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the image file
        image = Image.open(uploaded_file)

        # Display the image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.write("Image successfully uploaded and displayed.")

if __name__ == "__main__":
    main()
