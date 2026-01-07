"""
Send page for the WhatsApp Image Sender application.
"""
import streamlit as st
from utils.contact_manager import ContactManager
from utils.drive_handler import DriveHandler
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import math
import re
import json
import os
import base64
from streamlit_image_select import image_select
from st_clickable_images import clickable_images
import tempfile
from utils.telegram_sender import send_telegram_image
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Send Images - WhatsApp Image Sender",
    page_icon="🔄",
    layout="wide"
)

load_dotenv()

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

# Add custom CSS for beautification
st.markdown('''
    <style>
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4F8BF9;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .image-card {
        background: #f8fafd;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(79,139,249,0.07);
        padding: 1.1rem 1rem 0.7rem 1rem;
        margin-bottom: 1.2rem;
        border: 1.5px solid #e3e8f0;
    }
    .category-header {
        color: #2d3748;
        background: #e3e8f0;
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.7rem;
        margin-top: 0.7rem;
        letter-spacing: 0.5px;
    }
    .contact-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f4f7fa;
        border-radius: 7px;
        padding: 0.35rem 0.7rem 0.35rem 0.7rem;
        margin-bottom: 0.5rem;
        margin-top: 0.2rem;
        box-shadow: 0 1px 3px rgba(79,139,249,0.04);
        min-width: 0;
        overflow: hidden;
    }
    .contact-label {
        flex: 1 1 60%;
        font-size: 1.07rem;
        color: #e2e8f0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-right: 0.5rem;
    }
    .contact-checkbox {
        flex: 0 0 auto;
        margin-right: 0.5rem;
    }
    .contact-delete {
        flex: 0 0 auto;
        margin-left: 0.2rem;
    }
    .clickable-img-container {
        position: relative;
        display: inline-block;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: box-shadow 0.2s;
    }
    .clickable-img-container.selected {
        box-shadow: 0 0 0 4px #4F8BF9;
        border: 2.5px solid #4F8BF9;
    }
    .clickable-img-container .img-checkmark {
        display: none;
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 2rem;
        color: #4F8BF9;
        background: #fff;
        border-radius: 50%;
        padding: 0.1em 0.2em;
        box-shadow: 0 1px 4px rgba(79,139,249,0.13);
        z-index: 2;
    }
    .clickable-img-container.selected .img-checkmark {
        display: block;
    }
    </style>
''', unsafe_allow_html=True)

CONTACT_FILES = {
    "industrial_contacts": "industrial_contacts.json",
    "distributer_contacts": "distributer_contacts.json",
    "technician_contacts": "technician_contacts.json"
}

# Helper to load contacts from file
def load_contacts_from_file(category_key):
    file_path = CONTACT_FILES[category_key]
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

# Helper to save contacts to file
def save_contacts_to_file(category_key, contacts):
    file_path = CONTACT_FILES[category_key]
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def format_and_validate_number(number):
    number = number.replace(' ', '').replace('-', '')
    if number.startswith('+91'):
        num_part = number[3:]
    elif number.startswith('91'):
        number = '+' + number
        num_part = number[3:]
    elif len(number) == 10 and number.isdigit():
        number = '+91' + number
        num_part = number[3:]
    else:
        num_part = ''
    if re.fullmatch(r'\+91[6-9]\d{9}', number):
        return number, True
    else:
        return number, False

def add_contact(category_key, name, number):
    if name and number and not any(c['name'] == name and c['number'] == number for c in st.session_state[str(category_key)]):
        st.session_state[str(category_key)].append({'name': name, 'number': number, 'checked': True})
        save_contacts_to_file(str(category_key), st.session_state[str(category_key)])

def render_contact_section() -> None:
    """Render the contact selection section with tabs for categories and a unified add contact form always visible above the tabs."""
    st.subheader("Select Contacts by Category")

    # Define categories
    categories = [
        ("Industrial", "industrial_contacts"),
        ("Distributer", "distributer_contacts"),
        ("Technicians", "technician_contacts")
    ]
    category_labels = [label for label, _ in categories]
    category_key_map = {label: key for label, key in categories}

    # Add contact form (always visible, as before)
    with st.form("add_contact_form", clear_on_submit=True):
        new_name = st.text_input("Contact name", key="input_unified_name")
        new_number = st.text_input("Contact number (10 digits or with +91)", key="input_unified_number")
        add_category_label = st.selectbox("Select category to add contact", category_labels, key="select_category")
        submitted = st.form_submit_button("Add Contact")
        if submitted:
            formatted_number, valid = format_and_validate_number(new_number)
            if not valid:
                st.error("Please enter a valid Indian mobile number (10 digits, starts with 6-9) or with +91 prefix.")
            else:
                if add_category_label:
                    add_category_key = category_key_map[add_category_label]
                    add_contact(add_category_key, new_name, formatted_number)
                else:
                    st.warning("Please select a category to add the contact to.")

    # Tabs for category selection
    tab_objs = st.tabs(category_labels)

    # Show contacts and controls for the selected tab only
    for tab, (label, key) in zip(tab_objs, categories):
        if key is None:
            continue
        with tab:
            st.markdown(f"### {label}")
            if str(key) not in st.session_state:
                st.session_state[str(key)] = load_contacts_from_file(key)
            if f"{key}_master" not in st.session_state:
                st.session_state[f"{key}_master"] = True
            master_checked = st.checkbox(
                f"Select all {label}",
                value=st.session_state[f"{key}_master"],
                key=f"{key}_master_cb"
            )
            st.session_state[f"{key}_master"] = master_checked
            if st.session_state[str(key)]:
                if all(c['checked'] for c in st.session_state[str(key)]) != master_checked:
                    for c in st.session_state[str(key)]:
                        c['checked'] = master_checked
                to_delete = []
                for idx, contact in enumerate(st.session_state[str(key)]):
                    contact_cols = st.columns([7,1])
                    with contact_cols[0]:
                        st.markdown(f"<span style='font-size:1.07rem;color:#e2e8f0;'>{contact['name']} ({contact['number']})</span>", unsafe_allow_html=True)
                        delete_btn = st.button("Delete", key=f"{key}_del_{idx}")
                        if delete_btn:
                            to_delete.append(idx)
                    with contact_cols[1]:
                        checked = st.checkbox(
                            "",
                            value=contact['checked'],
                            key=f"{key}_cb_{idx}",
                            label_visibility="collapsed"
                        )
                        st.session_state[str(key)][idx]['checked'] = checked
                for idx in sorted(to_delete, reverse=True):
                    del st.session_state[str(key)][idx]
                save_contacts_to_file(str(key), st.session_state[str(key)])
                all_checked = all(c['checked'] for c in st.session_state[str(key)])
                none_checked = all(not c['checked'] for c in st.session_state[str(key)])
                if all_checked and not st.session_state[f"{key}_master"]:
                    st.session_state[f"{key}_master"] = True
                elif none_checked and st.session_state[f"{key}_master"]:
                    st.session_state[f"{key}_master"] = False
            else:
                st.info(f"No {label.lower()} contacts added yet.")
    # For downstream use: collect all selected contacts
    selected_contacts = []
    for _, key in categories:
        selected_contacts.extend([
            c for c in st.session_state.get(str(key), []) if c['checked']
        ])
    st.session_state['selected_contacts'] = selected_contacts

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

def display_image_grid_with_clickable_only(images, creds, image_type, show_all):
    """Display images in a 2x2 grid layout. Each image has a checkbox below it for selection. No button, no form. Show all or only the latest two."""
    if not show_all:
        images = images[:2]
    if f'selected_{image_type}_images' not in st.session_state:
        st.session_state[f'selected_{image_type}_images'] = set()
    selected_images = st.session_state[f'selected_{image_type}_images']

    # Minimal, clean CSS for image grid
    st.markdown("""
    <style>
    .img-row { display: flex; gap: 1.5rem; margin-bottom: 1.2rem; }
    .img-minimal-img {
        width: 100%;
        border-radius: 8px;
        display: block;
        border: 2.5px solid #2563eb11;
        margin-bottom: 0.3rem;
    }
    .img-minimal-img.selected {
        border: 2.5px solid #2563eb;
    }
    .img-minimal-caption {
        font-size: 1rem;
        color: #22223b;
        margin: 0.4rem 0 0.1rem 0;
        text-align: left;
        font-weight: 500;
    }
    .img-minimal-meta {
        font-size: 0.93rem;
        color: #64748b;
        margin-bottom: 0.2rem;
        margin-top: 0.1rem;
        text-align: left;
    }
    @media (max-width: 900px) {
        .img-row { flex-direction: column; gap: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    for i in range(0, len(images), 2):
        st.markdown('<div class="img-row">', unsafe_allow_html=True)
        cols = st.columns(2)
        for col, idx in zip(cols, [i, i+1]):
            if idx < len(images):
                img = images[idx]
                is_selected = img['id'] in selected_images
                img_bytes = None
                try:
                    img_bytes = get_image_bytes(img['id'], creds)
                except Exception as e:
                    col.error("Could not load image preview")
                img_b64 = base64.b64encode(img_bytes).decode() if img_bytes else ""
                img_class = "img-minimal-img selected" if is_selected else "img-minimal-img"
                col.markdown(f"<img src='data:image/png;base64,{img_b64}' class='{img_class}' alt='image'>", unsafe_allow_html=True)
                cb_key = f"cb_{image_type}_{img['id']}"
                checked = col.checkbox("Select", value=is_selected, key=cb_key)
                if checked and not is_selected:
                    selected_images.add(img['id'])
                elif not checked and is_selected:
                    selected_images.discard(img['id'])
                col.markdown(f"<div class='img-minimal-caption'>{img['name']}</div>", unsafe_allow_html=True)
                col.markdown(f"<div class='img-minimal-meta'>Size: {img['size']} bytes<br>Uploaded: {format_date(img['createdTime'])}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Main page content
st.markdown('<div class="section-header">Send Images</div>', unsafe_allow_html=True)

# Contact selection section
render_contact_section()

st.markdown("---")

# Image selection section
st.markdown('<div class="section-header">Select Image</div>', unsafe_allow_html=True)

# Create tabs for Normal and Generated Images
tab1, tab2 = st.tabs(["Normal Images", "Generated Images"])

# Get credentials once to reuse
creds = DriveHandler._get_credentials()

# Remove the input fields for Telegram bot token and chat ID
bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

with tab1:
    st.markdown('<div class="category-header">Normal Images</div>', unsafe_allow_html=True)
    normal_images = DriveHandler.list_drive_images("normal_images")
    if normal_images:
        if 'show_all_normal' not in st.session_state:
            st.session_state['show_all_normal'] = False
        show_all = st.session_state['show_all_normal']
        display_image_grid_with_clickable_only(normal_images, creds, "normal", show_all)
        if not show_all and len(normal_images) > 2:
            if st.button("👁️ Show All Images", key="show_all_normal_btn"):
                st.session_state['show_all_normal'] = True
                st.experimental_rerun()
        elif show_all and len(normal_images) > 2:
            if st.button("👁️ Show Only Latest 2 Images", key="show_latest_normal_btn"):
                st.session_state['show_all_normal'] = False
                st.experimental_rerun()
        # --- Normal Images Send Button ---
        send_normal = st.button("\U0001F4E4 Send Selected Images to Selected Contacts", key="send_normal_btn")
        if send_normal and not st.session_state.get("normal_sent", False):
            st.session_state["normal_sent"] = True
            selected_contacts = st.session_state.get('selected_contacts', [])
            selected_ids = st.session_state['selected_normal_images']
            if not selected_contacts:
                st.warning("Please select at least one contact.")
            elif not selected_ids:
                st.warning("Please select at least one image.")
            elif not bot_token or not chat_id:
                st.warning("Please enter your Telegram Bot Token and Chat ID.")
            else:
                contact_numbers = [c['number'] for c in selected_contacts]
                image_details = []
                import tempfile
                import shutil
                temp_dir = tempfile.mkdtemp()
                try:
                    for img in normal_images:
                        if img['id'] in selected_ids:
                            img_bytes = get_image_bytes(img['id'], creds)
                            img_path = os.path.join(temp_dir, f"{img['name']}")
                            with open(img_path, "wb") as f:
                                f.write(img_bytes)
                            image_details.append({"path": img_path, "name": img['name']})
                    total = len(contact_numbers) * len(image_details)
                    progress = st.progress(0, text="Sending images via Telegram...")
                    count = 0
                    for number in contact_numbers:
                        for image in image_details:
                            try:
                                send_telegram_image(bot_token, chat_id, image['path'], caption=image['name'])
                                count += 1
                                progress.progress(count / total, text=f"Sent {count} of {total}...")
                            except Exception as e:
                                st.error(f"Failed to send to {number}: {e}")
                    progress.empty()
                    st.success("All images sent!")
                except Exception as e:
                    st.error(f"Failed to send images: {e}")
                finally:
                    shutil.rmtree(temp_dir)
            st.session_state["normal_sent"] = False
    else:
        st.info("No normal images found")

with tab2:
    st.markdown('<div class="category-header">Generated Images</div>', unsafe_allow_html=True)
    generated_images = DriveHandler.list_drive_images("generated_images")
    if generated_images:
        if 'show_all_generated' not in st.session_state:
            st.session_state['show_all_generated'] = False
        show_all = st.session_state['show_all_generated']
        display_image_grid_with_clickable_only(generated_images, creds, "generated", show_all)
        if not show_all and len(generated_images) > 2:
            if st.button("👁️ Show All Images", key="show_all_generated_btn"):
                st.session_state['show_all_generated'] = True
                st.experimental_rerun()
        elif show_all and len(generated_images) > 2:
            if st.button("👁️ Show Only Latest 2 Images", key="show_latest_generated_btn"):
                st.session_state['show_all_generated'] = False
                st.experimental_rerun()
        # --- Generated Images Send Button ---
        send_generated = st.button("\U0001F4E4 Send Selected Images to Selected Contacts", key="send_generated_btn")
        if send_generated and not st.session_state.get("generated_sent", False):
            st.session_state["generated_sent"] = True
            selected_contacts = st.session_state.get('selected_contacts', [])
            selected_ids = st.session_state['selected_generated_images']
            if not selected_contacts:
                st.warning("Please select at least one contact.")
            elif not selected_ids:
                st.warning("Please select at least one image.")
            else:
                # Optionally, you can add a simple info or progress message here
                pass
                contact_numbers = [c['number'] for c in selected_contacts]
                image_details = []
                import tempfile
                import shutil
                temp_dir = tempfile.mkdtemp()
                try:
                    for img in generated_images:
                        if img['id'] in selected_ids:
                            img_bytes = get_image_bytes(img['id'], creds)
                            img_path = os.path.join(temp_dir, f"{img['name']}")
                            with open(img_path, "wb") as f:
                                f.write(img_bytes)
                            image_details.append({"path": img_path, "name": img['name']})
                    total = len(contact_numbers) * len(image_details)
                    progress = st.progress(0, text="Sending images via Telegram...")
                    count = 0
                    for number in contact_numbers:
                        for image in image_details:
                            try:
                                send_telegram_image(bot_token, chat_id, image['path'], caption=image['name'])
                                count += 1
                                progress.progress(count / total, text=f"Sent {count} of {total}...")
                            except Exception as e:
                                st.error(f"Failed to send to {number}: {e}")
                    progress.empty()
                    st.success("All images sent!")
                except Exception as e:
                    st.error(f"Failed to send images: {e}")
                finally:
                    shutil.rmtree(temp_dir)
            st.session_state["generated_sent"] = False
    else:
        st.info("No generated images found")

# Add section for sending plain text messages
# st.markdown('<div class="section-header">Send Text Message</div>', unsafe_allow_html=True)
# text_message = st.text_area("Enter your message", key="plain_text_message")
# if st.button("Send Text Message to Selected Contacts", key="send_text_btn"):
#     selected_contacts = st.session_state.get('selected_contacts') or []
#     if not selected_contacts:
#         st.warning("Please select at least one contact.")
#     elif not text_message.strip():
#         st.warning("Please enter a message.")
#     else:
#         for contact in selected_contacts:
#             try:
#                 send_whatsapp_message(contact['number'], text_message)
#                 st.success(f"Message sent to {contact['name']}")
#             except Exception as e:
#                 st.error(f"Failed to send message to {contact['name']}: {e}") 
                