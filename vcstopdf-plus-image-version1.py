import streamlit as st
from PIL import Image
from fpdf2 import FPDF
import io

def main():
    st.title("Image Upload Application")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the image file
        image = Image.open(uploaded_file)

        # Display the image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        st.write("Image successfully uploaded and displayed.")

        # Save the image to a PDF
        pdf = FPDF()
        pdf.add_page()
        img_temp = io.BytesIO()
        image.save(img_temp, format="PNG")
        img_temp.seek(0)
        pdf.image(img_temp, x=10, y=10, w=190)  # Adjust dimensions as necessary

        # Create a button to download the PDF
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        st.download_button(
            label="Download Image as PDF",
            data=pdf_output,
            file_name="uploaded_image.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
