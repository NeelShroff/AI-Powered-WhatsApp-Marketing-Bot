"""
Main application file for the WhatsApp Image Sender.
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="WhatsApp Image Sender",
    page_icon="📱",
    layout="wide"
)

# Custom CSS for mobile optimization
st.markdown("""
    <style>
    /* Mobile-friendly styles */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
        }
    }
    
    /* General styles */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Main content
st.title("Welcome to WhatsApp Image Sender")

st.markdown("""
This application helps you manage and send images via WhatsApp. You can:

1. 🔄 **Send Images**: Select contacts and send images via WhatsApp
2. ⬆️ **Upload Images**: Upload images to Google Drive for storage
3. 🖼️ **Gallery**: View and manage your uploaded images

Use the sidebar to navigate between pages.
""")


