# Import the necessary modules
import streamlit as st
from io import BytesIO
import base64
from streamlit_ace import st_ace
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Function to create download PDF link
def create_download_link_pdf(pdf_data, download_filename):
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{download_filename}">Download PDF</a>'
    return href

# Initialize session states
st.session_state.setdefault("task_list", [])
st.session_state.setdefault("link_dict", {})
st.session_state.setdefault("file_dict", {})
st.session_state.setdefault("text_dict", {})
st.session_state.setdefault("code_dict", {})
st.session_state.setdefault("image_dict", {})

# Input fields
task = st.text_input("Enter your task:")
if st.button("Save Task"):
    st.session_state.task_list.append(task)

link = st.text_input("Enter a research link for the task:")
if st.button("Save Link"):
    st.session_state.link_dict.setdefault(task, []).append(link)

uploaded_file = st.file_uploader("Upload a document for the task:")
if st.button("Save File"):
    st.session_state.file_dict.setdefault(task, []).append(uploaded_file)

text = st.text_area("Enter text for the task:")
if st.button("Save Text"):
    st.session_state.text_dict.setdefault(task, []).append(text)

# Ace editor for code
code = st_ace(language="python", theme="monokai", key="ace-editor")
if st.button("Save Code"):
    st.session_state.code_dict.setdefault(task, []).append(code)

# Upload image
uploaded_image = st.file_uploader("Upload an image for the task:")
if st.button("Save Image"):
    st.session_state.image_dict.setdefault(task, []).append(uploaded_image)

# Display saved items
st.write("## Saved Items")
for task in st.session_state.task_list:
    st.write(f"### Task: {task}")

    # Display links
    if task in st.session_state.link_dict:
        st.write("#### Links:")
        for link in st.session_state.link_dict[task]:
            st.write(f"- {link}")

    # Display uploaded files
    if task in st.session_state.file_dict:
        st.write("#### Files:")
        for file in st.session_state.file_dict[task]:
            st.write(f"- {file.name if file else 'Unknown'}")

    # Display text
    if task in st.session_state.text_dict:
        st.write("#### Text:")
        for text in st.session_state.text_dict[task]:
            st.write(f"- {text}")

    # Display code
    if task in st.session_state.code_dict:
        st.write("#### Code:")
        for code in st.session_state.code_dict[task]:
            code_paragraph_style = ParagraphStyle(
                name='CodeStyle', fontName='Courier', fontSize=8, leftIndent=10, rightIndent=10, leading=8, wordWrap='CJK'
            )
            code_paragraph = Preformatted(code, code_paragraph_style)
            st.markdown(f"```\n{code}\n```")

    # Display image
    if task in st.session_state.image_dict:
        st.write("#### Image:")
        for image in st.session_state.image_dict[task]:
            if image:
                st.image(image)

# Generate PDF
if st.button("Generate PDF"):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, leftMargin=36, rightMargin=36)
    styles = getSampleStyleSheet()

    # Create a list of elements for the PDF
    pdf_elements = []

    for task in st.session_state.task_list:
        pdf_elements.append(Paragraph(f"Task: {task}", styles['Heading1']))

        # Display links
        if task in st.session_state.link_dict:
            pdf_elements.append(Paragraph("Links:", styles['Heading2']))
            for link in st.session_state.link_dict[task]:
                pdf_elements.append(Paragraph(f"- {link}", styles['Normal']))

        # Display uploaded files
        if task in st.session_state.file_dict:
            pdf_elements.append(Paragraph("Files:", styles['Heading2']))
            for file in st.session_state.file_dict[task]:
                pdf_elements.append(Paragraph(f"- {file.name if file else 'Unknown'}", styles['Normal']))

        # Display text
        if task in st.session_state.text_dict:
            pdf_elements.append(Paragraph("Text:", styles['Heading2']))
            for text in st.session_state.text_dict[task]:
                pdf_elements.append(Paragraph(f"- {text}", styles['Normal']))

        # Display code
        if task in st.session_state.code_dict:
            pdf_elements.append(Paragraph("Code:", styles['Heading2']))
            for code in st.session_state.code_dict[task]:
                code_paragraph_style = ParagraphStyle(
                    name='CodeStyle', fontName='Courier', fontSize=8, leftIndent=10, rightIndent=10, leading=8, wordWrap='CJK'
                )
                # Set a fixed width for code block to enable wrapping
                code_paragraph = Preformatted(code, code_paragraph_style, maxLineLength=65)  # Adjust maxLineLength as needed
                pdf_elements.append(code_paragraph)
                pdf_elements.append(Spacer(1, 10))  # Add spacing after code

        # Display image
        if task in st.session_state.image_dict:
            pdf_elements.append(Paragraph("Image:", styles['Heading2']))
            for image in st.session_state.image_dict[task]:
                if image:
                    pdf_elements.append(Image(image, width=200, height=200))  # Adjust image size as needed
                    pdf_elements.append(Spacer(1, 10))  # Add spacing after image

    # Build the PDF document
    doc.build(pdf_elements)

    # Output the PDF content to the BytesIO buffer
    pdf_buffer.seek(0)
    pdf_data = pdf_buffer.read()

    # Create a download link for the PDF
    st.markdown(create_download_link_pdf(pdf_data, "your_file.pdf"), unsafe_allow_html=True)
