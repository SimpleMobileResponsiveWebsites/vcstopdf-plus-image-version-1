import os
import uuid
from datetime import datetime
import tempfile
import sys
import traceback
import logging

logging.basicConfig(level=logging.INFO)

try:
    import pandas as pd
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
except ImportError as e:
    logging.error(f"Error importing libraries: {e}")
    logging.error(traceback.format_exc())

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
            logging.error(f"Error initializing session state: {e}")
            logging.error(traceback.format_exc())

    def render_app(self):
        """Main application rendering method"""
        try:
            st.title("Advanced Documentation & Testing App")

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
            logging.error(f"Critical error in rendering app: {e}")
            logging.error(traceback.format_exc())

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
            logging.error(f"Error in version section: {e}")
            logging.error(traceback.format_exc())

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
        logging.error(f"Unhandled error in main application: {e}")
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
