"""
Upload Navigation page for the WhatsApp Image Sender application.
This page serves as a hub to navigate between different upload types.
"""
import streamlit as st
from utils.drive_handler import DriveHandler
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Upload Images - WhatsApp Image Sender",
    page_icon="⬆️",
    layout="wide"
)

# Enhanced CSS for modern, clean design
st.markdown("""
    <style>
    .page-header {
        text-align: center;
        margin-bottom: 40px;
        padding: 30px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .page-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .page-header p {
        font-size: 1.1rem;
        margin: 10px 0 0 0;
        opacity: 0.9;
    }
    .upload-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .upload-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    .upload-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .card-icon {
        font-size: 2.5rem;
        margin-right: 15px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    .card-description {
        color: #7f8c8d;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0 0 25px 0;
    }
    .feature-list li {
        padding: 8px 0;
        color: #34495e;
        position: relative;
        padding-left: 25px;
    }
    .feature-list li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #27ae60;
        font-weight: bold;
        font-size: 1.1rem;
    }
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 2rem;
        }
        .upload-card {
            padding: 20px;
            margin: 15px 0;
        }
        .card-title {
            font-size: 1.3rem;
        }
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'upload_view' not in st.session_state:
    st.session_state.upload_view = 'main'

def format_date(date_str):
    """Format ISO date string to 'Day Month Year'."""
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.strftime('%d %B %Y')

def show_normal_upload():
    """Show normal image upload interface."""
    st.title("📸 Upload Normal Images")
    
    st.markdown("""
    Upload your normal images here. These images will be stored in the normal_images folder 
    and can be used for sending via WhatsApp.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        
        # Display image preview
        st.image(uploaded_file, caption='Preview', use_column_width=True)
        
        # Upload button
        if st.button("Upload to Drive"):
            try:
                with st.spinner("Uploading..."):
                    file_data = uploaded_file.getvalue()
                    result = DriveHandler.upload_to_drive(file_data, "normal_images", uploaded_file.name)
                    
                    if result:
                        st.success("Normal image uploaded successfully!")
                        st.json(result)
                    else:
                        st.error("Failed to upload image")
                    st.rerun()
            except Exception as e:
                st.error(f"Error during upload: {str(e)}")
    
    # Recent uploads
    st.markdown("---")
    st.subheader("Recent Normal Image Uploads")
    
    images = DriveHandler.list_drive_images("normal_images")
    if images:
        for img in images[:10]:
            formatted_date = format_date(img['createdTime'])
            if st.button(f"📸 {img['name']} ({formatted_date})", key=f"normal_{img['id']}"):
                st.session_state.selected_image = {
                    'id': img['id'],
                    'folder_type': 'normal_images',
                    'name': img['name']
                }
                st.switch_page("pages/3_🖼️_Gallery.py")
    else:
        st.info("No normal images uploaded yet")

def show_generated_upload():
    """Show generated image upload interface."""
    st.title("🎨 Upload Generated Images")
    
    st.markdown("""
    Upload your generated/AI-created images here. These images will be stored in the generated_images folder 
    and can be used for sending via WhatsApp.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a generated image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        
        # Display image preview
        st.image(uploaded_file, caption='Preview', use_column_width=True)
        
        # Upload button
        if st.button("Upload to Drive"):
            try:
                with st.spinner("Uploading..."):
                    file_data = uploaded_file.getvalue()
                    result = DriveHandler.upload_to_drive(file_data, "generated_images", uploaded_file.name)
                    
                    if result:
                        st.success("Generated image uploaded successfully!")
                        st.json(result)
                    else:
                        st.error("Failed to upload image")
                    st.rerun()
            except Exception as e:
                st.error(f"Error during upload: {str(e)}")
    
    # Recent uploads
    st.markdown("---")
    st.subheader("Recent Generated Image Uploads")
    
    images = DriveHandler.list_drive_images("generated_images")
    if images:
        for img in images[:10]:
            formatted_date = format_date(img['createdTime'])
            if st.button(f"🎨 {img['name']} ({formatted_date})", key=f"generated_{img['id']}"):
                st.session_state.selected_image = {
                    'id': img['id'],
                    'folder_type': 'generated_images',
                    'name': img['name']
                }
                st.switch_page("pages/3_🖼️_Gallery.py")
    else:
        st.info("No generated images uploaded yet")

# Main page content
if st.session_state.upload_view == 'main':
    st.markdown("""
        <div class="page-header">
            <h1>⬆️ Upload Images</h1>
            <p>Choose the type of images you want to upload. Each type has its own dedicated page with specific features.</p>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for the upload options
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="upload-card">
            <div class="card-header">
                <div class="card-icon">📸</div>
                <h3 class="card-title">Normal Images</h3>
            </div>
            <p class="card-description">Upload regular photos and images from your device for everyday use.</p>
            <ul class="feature-list">
                <li>Photos from camera</li>
                <li>Screenshots</li>
                <li>Downloaded images</li>
                <li>Personal photos</li>
                <li>Business documents</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📸 Upload Normal Images", key="normal_upload"):
            st.session_state.upload_view = 'normal'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="upload-card">
            <div class="card-header">
                <div class="card-icon">🎨</div>
                <h3 class="card-title">Generated Images</h3>
            </div>
            <p class="card-description">Upload AI-generated or creatively designed images for special projects.</p>
            <ul class="feature-list">
                <li>AI-generated images</li>
                <li>Created graphics</li>
                <li>Design work</li>
                <li>Generated content</li>
                <li>Creative projects</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎨 Upload Generated Images", key="generated_upload"):
            st.session_state.upload_view = 'generated'
            st.rerun()

elif st.session_state.upload_view == 'generated':
    if st.button("← Back to Upload Options"):
        st.session_state.upload_view = 'main'
        st.rerun()
    show_generated_upload()

elif st.session_state.upload_view == 'normal':
    if st.button("← Back to Upload Options"):
        st.session_state.upload_view = 'main'
        st.rerun()
    show_normal_upload() 