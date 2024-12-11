import streamlit as st
import os
import uuid
from datetime import datetime
from io import BytesIO
import tempfile
import sys
import traceback

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
        # Add system information logging
        self._log_system_info()
        
        # Temporary directories for cloud compatibility
        self.temp_dir = tempfile.gettempdir()

        # Initialize session state
        self._initialize_session_state()

    def _log_system_info(self):
        """Log system and library versions for debugging"""
        st.sidebar.header("System Information")
        st.sidebar.write(f"Python Version: {sys.version}")
        st.sidebar.write(f"Streamlit Version: {st.__version__}")
        st.sidebar.write(f"Pandas Version: {pd.__version__}")

    def _initialize_session_state(self):
        """Initialize all required session states with checks"""
        try:
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
        except Exception as e:
            st.error(f"Error initializing session state: {e}")
            st.error(traceback.format_exc())

    def save_uploaded_image(self, uploaded_file, app_version):
        """Save uploaded image with unique filename and validation"""
        try:
            if uploaded_file is not None:
                # Validate and save image
                img = Image.open(uploaded_file)
                img.verify()  # Verify the image is not corrupted

                # Generate unique filename
                unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
                version_dir = os.path.join(self.temp_dir, app_version)
                os.makedirs(version_dir, exist_ok=True)
                filepath = os.path.join(version_dir, unique_filename)

                # Save the image
                img = Image.open(uploaded_file)
                img.save(filepath)

                return filepath
        except Exception as e:
            st.error(f"Error saving image: {e}")
            st.error(traceback.format_exc())
            return None
        return None

    def render_app(self):
        """Main application rendering method"""
        try:
            st.title("Advanced Documentation & Testing App")

            # Add a welcome message and basic instructions
            st.info("""
            Welcome to the Documentation App! 
            - Start by entering an App Version
            - Use the expandable sections to add content
            - Export your documentation when ready
            """)

            # Version and Metrics Section
            with st.expander("Version & Metrics", expanded=True):
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

        except Exception as e:
            st.error(f"Critical error in rendering app: {e}")
            st.error(traceback.format_exc())

    def _render_version_section(self):
        """Render version input and metrics section"""
        try:
            col1, col2 = st.columns(2)
            with col1:
                app_version = st.text_input("App Version:", key="app_version_input")
            with col2:
                interpreter_version = st.text_input("Interpreter Version:", key="interpreter_version_input")

            if st.button("Save Version Information"):
                if app_version:
                    if app_version not in st.session_state.task_list:
                        st.session_state.task_list.append(app_version)
                    st.session_state.interpreter_dict[app_version] = {
                        'version': interpreter_version,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.success("Version information saved!")
                else:
                    st.warning("Please enter an App Version")
        except Exception as e:
            st.error(f"Error in version section: {e}")
            st.error(traceback.format_exc())

    def _render_image_upload_section(self):
        """Render image upload functionality"""
        try:
            app_version = st.text_input("Select Version for Image Upload:", key="image_upload_version")

            if app_version:
                uploaded_images = st.file_uploader(
                    "Upload Images", 
                    type=['png', 'jpg', 'jpeg', 'gif', 'bmp'], 
                    accept_multiple_files=True,
                    key="image_uploader"
                )

                if uploaded_images:
                    for img in uploaded_images:
                        saved_path = self.save_uploaded_image(img, app_version)
                        if saved_path:
                            if app_version not in st.session_state.images_dict:
                                st.session_state.images_dict[app_version] = []
                            st.session_state.images_dict[app_version].append(saved_path)
                            st.success(f"Image {img.name} saved successfully!")
            else:
                st.info("Enter a version to upload images")
        except Exception as e:
            st.error(f"Error in image upload section: {e}")
            st.error(traceback.format_exc())

    def _render_code_and_terminal_section(self):
        """Render code and terminal sections"""
        try:
            app_version = st.text_input("Version for Code/Terminal Entry:", key="code_terminal_version")

            if app_version:
                # Code input
                code = st_ace(
                    language="python", 
                    theme="monokai", 
                    min_lines=10,
                    key="code_editor"
                )

                # Terminal/Log input
                terminal_output = st.text_area("Terminal/Log Output", key="terminal_output")

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
            else:
                st.info("Enter a version to save code and terminal output")
        except Exception as e:
            st.error(f"Error in code and terminal section: {e}")
            st.error(traceback.format_exc())

    def _display_saved_items(self):
        """Display all saved items with version filtering"""
        try:
            app_version = st.selectbox("Select Version to Display", 
                                       ['All'] + st.session_state.task_list)

            versions_to_display = st.session_state.task_list if app_version == 'All' else [app_version]

            if not versions_to_display:
                st.info("No versions saved yet. Enter a version to start documenting.")
                return

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
        except Exception as e:
            st.error(f"Error displaying saved items: {e}")
            st.error(traceback.format_exc())

    def _render_export_options(self):
        """Render export options for documentation"""
        try:
            export_type = st.radio("Export Documentation", 
                                    ["PDF", "Markdown", "HTML"])

            if st.button("Generate Document"):
                if not st.session_state.task_list:
                    st.warning("No versions to export. Please save some content first.")
                    return

                if export_type == "PDF":
                    self._generate_pdf()
                elif export_type == "Markdown":
                    self._generate_markdown()
                else:
                    self._generate_html()
        except Exception as e:
            st.error(f"Error in export options: {e}")
            st.error(traceback.format_exc())

    def _generate_pdf(self):
        """Generate comprehensive PDF documentation"""
        st.warning("PDF generation is not fully implemented yet.")

    def _generate_markdown(self):
        """Generate markdown documentation"""
        st.warning("Markdown generation is not fully implemented yet.")

    def _generate_html(self):
        """Generate HTML documentation"""
        st.warning("HTML generation is not fully implemented yet.")


def main():
    try:
        # Set page configuration
        st.set_page_config(
            page_title="Documentation App", 
            page_icon=":memo:", 
            layout="wide"
        )
        
        # Initialize and render the app
        app = DocumentationApp()
        app.render_app()
    
    except Exception as e:
        st.error(f"Unhandled error in main application: {e}")
        st.error(traceback.format_exc())


if __name__ == "__main__":
    main()
