"""
Normal Images Upload component for the WhatsApp Image Sender application.
"""
import streamlit as st
import sys
import os

# Add the parent directory to the path to import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.drive_handler import DriveHandler
from datetime import datetime

def show_normal_upload():
    """Display the normal image upload interface."""
    
    # Custom CSS for mobile optimization
    st.markdown("""
        <style>
        @media (max-width: 768px) {
            .stButton button {
                width: 100%;
            }
            .stUploadedFile {
                width: 100%;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    def format_date(date_str):
        """Format ISO date string to 'Day Month Year'."""
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d %B %Y')

    def handle_upload():
        """Handle file upload and processing for normal images."""
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
            st.write(file_details)
            
            # Display image preview
            st.image(uploaded_file, caption='Preview', use_column_width=True)
            
            # Upload button
            if st.button("Upload to Drive"):
                try:
                    # Show progress
                    with st.spinner("Uploading..."):
                        file_data = uploaded_file.getvalue()
                        result = DriveHandler.upload_to_drive(file_data, "normal_images", uploaded_file.name)
                        
                        if result:
                            st.success("Normal image uploaded successfully!")
                            st.json(result)
                        else:
                            st.error("Failed to upload image")
                        st.rerun()  # Using rerun instead of experimental_rerun
                except Exception as e:
                    st.error(f"Error during upload: {str(e)}")

    def render_upload_section() -> None:
        """Render the normal image upload section."""
        handle_upload()

    def render_recent_uploads() -> None:
        """Render the recent normal image uploads section."""
        st.subheader("Recent Normal Image Uploads")
        
        images = DriveHandler.list_drive_images("normal_images")
        if images:
            for img in images[:10]:  # Show last 10 uploads
                formatted_date = format_date(img['createdTime'])
                # Make the image name clickable
                if st.button(f"📸 {img['name']} ({formatted_date})", key=f"normal_{img['id']}"):
                    # Store the selected image info in session state
                    st.session_state.selected_image = {
                        'id': img['id'],
                        'folder_type': 'normal_images',
                        'name': img['name']
                    }
                    # Navigate to Gallery page
                    st.switch_page("pages/3_🖼️_Gallery.py")
        else:
            st.info("No normal images uploaded yet")

    # Main page content
    st.title("📸 Upload Normal Images")

    st.markdown("""
    Upload your normal images here. These images will be stored in the normal_images folder 
    and can be used for sending via WhatsApp.
    """)

    # Upload section
    render_upload_section()

    st.markdown("---")

    # Recent uploads section
    render_recent_uploads() 