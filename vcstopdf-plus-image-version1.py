import streamlit as st
import base64
import os
import uuid
from datetime import datetime
from io import BytesIO

import pandas as pd
import plotly.express as px
from PIL import Image

from streamlit_ace import st_ace
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, 
    Preformatted, Image as PDFImage, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class DocumentationApp:
    def __init__(self):
        # Ensure necessary directories exist
        self.IMAGES_DIR = "uploaded_images"
        self.BACKUP_DIR = "backups"
        os.makedirs(self.IMAGES_DIR, exist_ok=True)
        os.makedirs(self.BACKUP_DIR, exist_ok=True)

        # Initialize session state
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize all required session states with checks"""
        default_states = {
            'task_list': [],
            'text_dict': {},
            'code_dict': {},
            'interpreter_dict': {},
            'terminal_dict': {},
            'images_dict': {},
            'metrics_dict': {},
            'logs_dict': {}
        }

        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def save_uploaded_image(self, uploaded_file, app_version):
        """Save uploaded image with unique filename and validation"""
        if uploaded_file is not None:
            try:
                # Validate image
                img = Image.open(uploaded_file)
                img.verify()  # Verify the image is not corrupted

                # Create version-specific directory
                version_dir = os.path.join(self.IMAGES_DIR, app_version)
                os.makedirs(version_dir, exist_ok=True)

                # Generate unique filename
                unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
                filename = os.path.join(version_dir, unique_filename)

                # Save the file
                img = Image.open(uploaded_file)
                img.save(filename)

                return filename
            except Exception as e:
                st.error(f"Error saving image: {e}")
                return None
        return None

    def render_app(self):
        """Main application rendering method"""
        st.title("Advanced Documentation & Testing App")

        # Version and Metrics Section
        with st.expander("Version & Metrics"):
            self._render_version_section()

        # Image Upload Section
        with st.expander("Image Management"):
            self._render_image_upload_section()

        # Code and Terminal Sections
        with st.expander("Code & Terminal Logs"):
            self._render_code_and_terminal_section()

        # Display and Export Section
        with st.expander("Saved Documentation"):
            self._display_saved_items()
            self._render_export_options()

    def _render_version_section(self):
        """Render version input and metrics section"""
        col1, col2 = st.columns(2)
        with col1:
            app_version = st.text_input("App Version:")
        with col2:
            interpreter_version = st.text_input("Interpreter Version:")

        if st.button("Save Version Information"):
            if app_version:
                if app_version not in st.session_state.task_list:
                    st.session_state.task_list.append(app_version)
                st.session_state.interpreter_dict[app_version] = {
                    'version': interpreter_version,
                    'timestamp': datetime.now().isoformat()
                }
                st.success("Version information saved!")

    def _render_image_upload_section(self):
        """Render image upload functionality"""
        app_version = st.text_input("Select Version for Image Upload:")
        
        if app_version:
            uploaded_images = st.file_uploader(
                "Upload Images", 
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'], 
                accept_multiple_files=True
            )

            if uploaded_images:
                for img in uploaded_images:
                    if st.button(f"Save {img.name}"):
                        saved_path = self.save_uploaded_image(img, app_version)
                        if saved_path:
                            if app_version not in st.session_state.images_dict:
                                st.session_state.images_dict[app_version] = []
                            st.session_state.images_dict[app_version].append(saved_path)
                            st.success(f"Image {img.name} saved successfully!")

    def _render_code_and_terminal_section(self):
        """Render code and terminal sections"""
        app_version = st.text_input("Version for Code/Terminal Entry:")
        
        if app_version:
            # Code input
            code = st_ace(
                language="python", 
                theme="monokai", 
                min_lines=10,
                key="code_editor"
            )

            # Terminal/Log input
            terminal_output = st.text_area("Terminal/Log Output")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Code"):
                    if app_version not in st.session_state.code_dict:
                        st.session_state.code_dict[app_version] = []
                    st.session_state.code_dict[app_version].append(code)
                    st.success("Code saved!")

            with col2:
                if st.button("Save Terminal Output"):
                    if app_version not in st.session_state.terminal_dict:
                        st.session_state.terminal_dict[app_version] = []
                    st.session_state.terminal_dict[app_version].append(terminal_output)
                    st.success("Terminal output saved!")

    def _display_saved_items(self):
        """Display all saved items with version filtering"""
        app_version = st.selectbox("Select Version to Display", 
                                   ['All'] + st.session_state.task_list)

        versions_to_display = st.session_state.task_list if app_version == 'All' else [app_version]

        for version in versions_to_display:
            st.subheader(f"Version: {version}")
            
            # Display images
            if version in st.session_state.images_dict:
                st.write("Images:")
                for img_path in st.session_state.images_dict[version]:
                    st.image(img_path, use_column_width=True)

            # Display code sections
            if version in st.session_state.code_dict:
                st.write("Code Sections:")
                for i, code in enumerate(st.session_state.code_dict[version], 1):
                    st.code(code, language="python")

            # Display terminal outputs
            if version in st.session_state.terminal_dict:
                st.write("Terminal Outputs:")
                for output in st.session_state.terminal_dict[version]:
                    st.text(output)

    def _render_export_options(self):
        """Render export options for documentation"""
        export_type = st.radio("Export Documentation", 
                                ["PDF", "Markdown", "HTML"])

        if st.button("Generate Document"):
            if export_type == "PDF":
                self._generate_pdf()
            elif export_type == "Markdown":
                self._generate_markdown()
            else:
                self._generate_html()

    def _generate_pdf(self):
        """Generate comprehensive PDF documentation"""
        # PDF generation logic similar to previous implementation
        # Add more robust error handling and comprehensive content capture

    def _generate_markdown(self):
        """Generate markdown documentation"""
        # Markdown generation logic

    def _generate_html(self):
        """Generate HTML documentation"""
        # HTML generation logic

def main():
    app = DocumentationApp()
    app.render_app()

if __name__ == "__main__":
    main()
