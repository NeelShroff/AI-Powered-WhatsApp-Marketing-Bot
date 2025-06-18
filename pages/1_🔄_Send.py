"""
Send page for the WhatsApp Image Sender application.
"""
import streamlit as st
from utils.contact_manager import ContactManager
from utils.drive_handler import DriveHandler
from utils.whatsapp_handler import WhatsAppHandler
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import math

# Page configuration
st.set_page_config(
    page_title="Send Images - WhatsApp Image Sender",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS for mobile optimization and link styling
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
        }
        .stSelectbox, .stMultiselect {
            width: 100%;
        }
    }
    .whatsapp-link {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
    .whatsapp-link:hover {
        background-color: #128C7E;
    }
    </style>
""", unsafe_allow_html=True)

def render_contact_section() -> None:
    """Render the contact selection section."""
    st.subheader("Select Contacts")
    
    # Get available contacts
    contacts = ContactManager.get_contacts()
    selected_contacts = ContactManager.get_selected_contacts()
    
    # Contact selection
    contact_options = [ContactManager.format_contact_display(c) for c in contacts]
    selected_indices = [
        i for i, c in enumerate(contacts)
        if c in selected_contacts
    ]
    
    selected = st.multiselect(
        "Choose contacts to send to",
        contact_options,
        default=[contact_options[i] for i in selected_indices],
        key="contact_selector"
    )
    
    # Update selected contacts
    new_selected = [
        contacts[i] for i, opt in enumerate(contact_options)
        if opt in selected
    ]
    ContactManager.set_selected_contacts(new_selected)
    
    # Deselect all button
    if st.button("Deselect All"):
        ContactManager.set_selected_contacts([])
        st.experimental_rerun()

def format_date(date_str):
    """Format ISO date string to 'Day Month Year'."""
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.strftime('%d %B %Y')

def get_image_bytes(file_id, creds):
    """Get image bytes from Google Drive."""
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh.read()

def get_sharing_link(file_id, creds):
    """Get a shareable link for a Google Drive file."""
    service = build('drive', 'v3', credentials=creds)
    
    # Update file permissions to make it accessible via link
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()
    
    # Get the web view link
    file = service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()
    
    return file.get('webViewLink')

def display_whatsapp_links(whatsapp_links):
    """Display WhatsApp links in a grid."""
    cols = st.columns(2)
    for idx, link_data in enumerate(whatsapp_links):
        with cols[idx % 2]:
            st.markdown(
                f'<a href="{link_data["link"]}" target="_blank" class="whatsapp-link">'
                f'Send to {link_data["name"]}</a>',
                unsafe_allow_html=True
            )

def display_image_grid(images, creds):
    """Display images in a 2x2 grid layout."""
    # Process images in pairs
    for i in range(0, len(images), 2):
        # Create a row with two columns
        col1, col2 = st.columns(2)
        
        # First image in the pair
        with col1:
            if i < len(images):
                img = images[i]
                formatted_date = format_date(img['createdTime'])
                try:
                    img_bytes = get_image_bytes(img['id'], creds)
                    st.image(img_bytes, caption=img['name'], use_column_width=True)
                except Exception as e:
                    st.error("Could not load image preview")
                st.write(f"**{img['name']}**")
                # Create two columns for size and date
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.write(f"Size: {img['size']} bytes")
                with info_col2:
                    st.write(f"Uploaded: {formatted_date}")
                # Send button
                if st.button("Send to WhatsApp", key=f"send_{img['id']}"):
                    selected_contacts = ContactManager.get_selected_contacts()
                    if not selected_contacts:
                        st.warning("Please select at least one contact first")
                    else:
                        # Get sharing link
                        drive_link = get_sharing_link(img['id'], creds)
                        # Generate WhatsApp links
                        whatsapp_links = WhatsAppHandler.send_to_whatsapp(
                            selected_contacts,
                            img['name'],
                            drive_link
                        )
                        if whatsapp_links:
                            st.success("Click the links below to send via WhatsApp:")
                            display_whatsapp_links(whatsapp_links)
        
        # Second image in the pair
        with col2:
            if i + 1 < len(images):
                img = images[i + 1]
                formatted_date = format_date(img['createdTime'])
                try:
                    img_bytes = get_image_bytes(img['id'], creds)
                    st.image(img_bytes, caption=img['name'], use_column_width=True)
                except Exception as e:
                    st.error("Could not load image preview")
                st.write(f"**{img['name']}**")
                # Create two columns for size and date
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.write(f"Size: {img['size']} bytes")
                with info_col2:
                    st.write(f"Uploaded: {formatted_date}")
                # Send button
                if st.button("Send to WhatsApp", key=f"send_{img['id']}_2"):
                    selected_contacts = ContactManager.get_selected_contacts()
                    if not selected_contacts:
                        st.warning("Please select at least one contact first")
                    else:
                        # Get sharing link
                        drive_link = get_sharing_link(img['id'], creds)
                        # Generate WhatsApp links
                        whatsapp_links = WhatsAppHandler.send_to_whatsapp(
                            selected_contacts,
                            img['name'],
                            drive_link
                        )
                        if whatsapp_links:
                            st.success("Click the links below to send via WhatsApp:")
                            display_whatsapp_links(whatsapp_links)
        
        # Add some spacing between rows
        st.write("---")

# Main page content
st.title("Send Images")

# Contact selection section
render_contact_section()

st.markdown("---")

# Image selection section
st.title("Select Image")

# Create tabs for Normal and Generated Images
tab1, tab2 = st.tabs(["Normal Images", "Generated Images"])

# Get credentials once to reuse
creds = DriveHandler._get_credentials()

with tab1:
    st.subheader("Normal Images")
    normal_images = DriveHandler.list_drive_images("normal_images")
    if normal_images:
        display_image_grid(normal_images, creds)
    else:
        st.info("No normal images found")

with tab2:
    st.subheader("Generated Images")
    generated_images = DriveHandler.list_drive_images("generated_images")
    if generated_images:
        display_image_grid(generated_images, creds)
    else:
        st.info("No generated images found") 