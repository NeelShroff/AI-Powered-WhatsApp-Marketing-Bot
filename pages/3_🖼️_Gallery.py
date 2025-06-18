"""
Beautiful Gallery page for the WhatsApp Image Sender application.
"""
import streamlit as st
from utils.drive_handler import DriveHandler
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import math

# Page configuration
st.set_page_config(
    page_title="Gallery - WhatsApp Bot",
    page_icon="🖼️",
    layout="wide"
)

# Clean, modern CSS
st.markdown("""
    <style>
    /* Modern font and base styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean header */
    .header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 12px;
        color: white;
    }
    
    .header h1 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    
    .header p {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Compact stats */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .stat-number {
        font-size: 1.25rem;
        font-weight: 600;
        color: #6366f1;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    /* Filter section - FIXED WHITE TEXT ISSUE */
    .filter-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        color: #1e293b !important; /* Added explicit text color */
    }
    
    /* Override Streamlit selectbox styling for better visibility */
    .filter-section .stSelectbox > div > div > div {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .filter-section .stSelectbox label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Force selectbox text color */
    .filter-section .stSelectbox div[data-baseweb="select"] {
        color: #1e293b !important;
    }
    
    .filter-section .stSelectbox div[data-baseweb="select"] > div {
        color: #1e293b !important;
        background-color: #f8fafc !important;
    }
    
    /* Selectbox dropdown styling */
    .filter-section .stSelectbox div[role="listbox"] {
        background-color: white !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .filter-section .stSelectbox div[role="option"] {
        color: #1e293b !important;
        background-color: white !important;
    }
    
    .filter-section .stSelectbox div[role="option"]:hover {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
    }
    
    /* Image grid - FIXED TO SHOW 2 IMAGES PER ROW */
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* Changed to exactly 2 columns */
        gap: 1.5rem; /* Increased gap for better spacing */
        padding: 0;
    }
    
    .image-card {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        max-width: 100%; /* Ensure cards don't exceed container */
    }
    
    .image-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .image-info {
        padding: 0.75rem;
    }
    
    .image-name {
        font-size: 0.9rem;
        font-weight: 500;
        color: #1e293b;
        margin-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .image-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: #ef4444 !important; /* Red color for delete button */
        color: white !important;
        border: none !important;
        padding: 0.5rem !important;
        font-size: 0.875rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #dc2626 !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        border-radius: 6px;
        background: #f8fafc;
        margin: 0 0.25rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: #6366f1 !important;
        background: #eff6ff !important;
        border: 1px solid #c7d2fe !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #6366f1 !important;
        background: #f1f5f9 !important;
    }
    
    /* Streamlit elements cleanup */
    .stSelectbox, .stTextInput {
        margin-bottom: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px;
    }
    
    /* Hide image captions and fix spacing issues */
    .stImage > div > div > div {
        display: none !important;
    }
    
    /* Ensure images fill their containers properly */
    .stImage > div {
        width: 100% !important;
    }
    
    /* Remove default streamlit spacing that might cause white bars */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0 !important;
    }
    
    /* Fix any unwanted margins in containers */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    /* Ensure consistent spacing */
    .stColumn {
        gap: 0 !important;
    }
    
    /* Remove extra spacing from info/warning messages */
    .stInfo, .stWarning, .stSuccess, .stError {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .gallery-grid {
            grid-template-columns: 1fr; /* Single column on mobile */
            gap: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
""", unsafe_allow_html=True)

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 1)
    return f"{s}{size_names[i]}"

def format_date(date_str):
    """Format date to readable format."""
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    now = datetime.now(dt.tzinfo)
    
    if dt.date() == now.date():
        return "Today"
    elif dt.date() == (now - timedelta(days=1)).date():
        return "Yesterday"
    elif (now - dt).days < 7:
        return dt.strftime('%A')
    else:
        return dt.strftime('%b %d')

def get_image_bytes(file_id, creds):
    """Get image bytes from Google Drive."""
    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def display_image_grid(images, creds):
    """Display images in a responsive grid with exactly 2 columns."""
    if not images:
        st.markdown("""
            <div style="
                text-align: center;
                padding: 2rem;
                background: #f8fafc;
                border-radius: 8px;
                border: 1px dashed #cbd5e1;
                color: #64748b;
                margin: 1rem 0;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📷</div>
                <div style="font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">No images found</div>
                <div style="font-size: 0.9rem;">Try adjusting your filters or upload some images.</div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Create two columns for the grid layout
    cols = st.columns(2, gap="large")
    
    for idx, img in enumerate(images):
        with cols[idx % 2]:  # Alternate between the two columns
            # Create a container for each image card
            with st.container():
                # Image display with proper container
                img_bytes = get_image_bytes(img['id'], creds)
                if img_bytes:
                    st.markdown("""
                        <div style="
                            background: white;
                            border-radius: 8px 8px 0 0;
                            border: 1px solid #e2e8f0;
                            border-bottom: none;
                            overflow: hidden;
                        ">
                    """, unsafe_allow_html=True)
                    st.image(img_bytes, use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Show placeholder if image fails to load
                    st.markdown("""
                        <div style="
                            background: #f1f5f9;
                            border: 1px solid #e2e8f0;
                            border-radius: 8px 8px 0 0;
                            border-bottom: none;
                            height: 200px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: #64748b;
                        ">
                            <div style="text-align: center;">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">❌</div>
                                <div>Failed to load image</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Image info in a compact card format
                st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 0.4rem 0.6rem;
                        border-radius: 0 0 8px 8px;
                        border: 1px solid #e2e8f0;
                        border-top: none;
                        margin-bottom: 0.3rem;
                        min-height: auto;
                    ">
                        <div style="
                            font-size: 0.85rem;
                            font-weight: 500;
                            color: #1e293b;
                            margin-bottom: 0.3rem;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            line-height: 1.2;
                        ">{img['name']}</div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            font-size: 0.7rem;
                            color: #64748b;
                            margin-bottom: 0.2rem;
                            line-height: 1.1;
                        ">
                            <span>{format_date(img['createdTime'])}</span>
                            <span>{format_file_size(int(img['size']))}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{img['id']}", use_container_width=True):
                    if DriveHandler.delete_from_drive(img["id"]):
                        st.success("Image deleted")
                        st.rerun()
                    else:
                        st.error("Failed to delete")
                
                # Add spacing between cards
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

def filter_images_by_time(images, time_filter):
    """Filter images based on time period."""
    now = datetime.now().replace(tzinfo=None)
    
    if time_filter == "All":
        return images
        
    filtered_images = []
    for img in images:
        img_date = datetime.fromisoformat(img['createdTime'].replace('Z', '+00:00'))
        img_date = img_date.replace(tzinfo=None)
        
        if time_filter == "Today":
            if img_date.date() == now.date():
                filtered_images.append(img)
        elif time_filter == "This Week":
            week_ago = now - timedelta(days=7)
            if img_date >= week_ago:
                filtered_images.append(img)
        elif time_filter == "This Month":
            if img_date.year == now.year and img_date.month == now.month:
                filtered_images.append(img)
        elif time_filter == "This Year":
            if img_date.year == now.year:
                filtered_images.append(img)
        elif str(time_filter).isdigit():
            if img_date.year == int(time_filter):
                filtered_images.append(img)
                
    return filtered_images

# Main content
st.markdown("""
    <div class="header">
        <h1>🖼️ Image Gallery</h1>
        <p>Browse and manage your images</p>
    </div>
""", unsafe_allow_html=True)

# Get all images
all_normal_images = DriveHandler.list_drive_images("normal_images")
all_generated_images = DriveHandler.list_drive_images("generated_images")

# Stats
total_size = sum(int(img['size']) for img in all_normal_images + all_generated_images)
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">{len(all_normal_images) + len(all_generated_images)}</div>
            <div class="stat-label">Total</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(all_normal_images)}</div>
            <div class="stat-label">Normal</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(all_generated_images)}</div>
            <div class="stat-label">Generated</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{format_file_size(total_size)}</div>
            <div class="stat-label">Size</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Filters - Using a more direct approach
st.markdown("### 🔍 Filters")
col1, col2 = st.columns(2)

with col1:
    time_filter = st.selectbox(
        "📅 Time Period",
        ["All", "Today", "This Week", "This Month", "This Year"]
    )

with col2:
    sort_by = st.selectbox(
        "🔄 Sort by",
        ["Newest First", "Oldest First", "Name (A-Z)", "Name (Z-A)"]
    )

# Tabs for image types
tab1, tab2 = st.tabs(["📸  Normal Images", "🎨  Generated Images"])

# Get credentials once
creds = DriveHandler._get_credentials()

with tab1:
    filtered_images = filter_images_by_time(all_normal_images, time_filter)
    
    if sort_by == "Newest First":
        filtered_images.sort(key=lambda x: x['createdTime'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_images.sort(key=lambda x: x['createdTime'])
    elif sort_by == "Name (A-Z)":
        filtered_images.sort(key=lambda x: x['name'].lower())
    elif sort_by == "Name (Z-A)":
        filtered_images.sort(key=lambda x: x['name'].lower(), reverse=True)
    
    display_image_grid(filtered_images, creds)

with tab2:
    filtered_images = filter_images_by_time(all_generated_images, time_filter)
    
    if sort_by == "Newest First":
        filtered_images.sort(key=lambda x: x['createdTime'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_images.sort(key=lambda x: x['createdTime'])
    elif sort_by == "Name (A-Z)":
        filtered_images.sort(key=lambda x: x['name'].lower())
    elif sort_by == "Name (Z-A)":
        filtered_images.sort(key=lambda x: x['name'].lower(), reverse=True)
    
    display_image_grid(filtered_images, creds)

