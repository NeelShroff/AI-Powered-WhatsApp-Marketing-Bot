"""
AI Poster Generator - 6-Step Workflow for WhatsApp Image Sender
"""
import streamlit as st
from typing import Optional, List
from PIL import Image
import io
import time
import base64
from utils.drive_handler import DriveHandler

def extract_text_from_image_api(image_bytes: bytes) -> str:
    # Placeholder for OpenAI OCR API call
    time.sleep(2)
    return "Sample extracted text from product detail image."

def generate_poster_api(product_image_bytes: bytes, extracted_text: str, requirements: str) -> bytes:
    # Placeholder for OpenAI image generation API call
    time.sleep(3)
    # Return a blank image for demo
    img = Image.new('RGB', (512, 384), color=(240, 240, 255))  # type: ignore
    return image_to_bytes(img)

def regenerate_poster_api(product_image_bytes: bytes, extracted_text: str, requirements: str, improvement_prompt: str) -> bytes:
    # Placeholder for OpenAI image regeneration API call
    time.sleep(3)
    img = Image.new('RGB', (512, 384), color=(220, 255, 220))  # type: ignore
    return image_to_bytes(img)

def image_to_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def bytes_to_image(img_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(img_bytes))

def upload_to_drive_api(image_bytes: bytes, filename: str) -> dict:
    # Placeholder for Google Drive upload
    time.sleep(2)
    # Use actual DriveHandler in production
    try:
        result = DriveHandler.upload_to_drive(image_bytes, "generated_images", filename)
        return result or {"success": False, "error": "Upload failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def show_generated_upload():
    # --- Session State Initialization ---
    def init_session():
        for k, v in {
            'step': 1,
            'detail_image': None,
            'detail_image_bytes': None,
            'detail_image_preview': None,
            'extracted_text': '',
            'extracted_text_confirmed': False,
            'requirements': '',
            'product_image': None,
            'product_image_bytes': None,
            'product_image_preview': None,
            'generated_poster_bytes': None,
            'generated_poster_versions': [],
            'improvement_prompt': '',
            'upload_result': None,
            'regenerating': False,
            'regeneration_prompts': [],
            'error': '',
        }.items():
            if k not in st.session_state:
                st.session_state[k] = v

    init_session()

    # --- Modern Horizontal Stepper Progress Bar ---
    steps = [
        "Upload Detail Image",
        "Extract Text",
        "Poster Requirements",
        "Upload Product Photo",
        "Generate Poster",
        "Review & Action"
    ]
    current = st.session_state.step
    stepper_html = """
    <style>
    .stepper-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2.5rem;
        margin-top: 1.5rem;
        user-select: none;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        min-width: 90px;
        position: relative;
    }
    .circle {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #e0e7ef;
        border: 3px solid #e0e7ef;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        color: #7b8794;
        margin-bottom: 0.3rem;
        transition: all 0.2s;
        z-index: 2;
    }
    .step.active .circle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        border: 3px solid #764ba2;
        box-shadow: 0 2px 12px rgba(102,126,234,0.15);
    }
    .step.completed .circle {
        background: #27ae60;
        color: #fff;
        border: 3px solid #27ae60;
        box-shadow: 0 2px 12px rgba(39,174,96,0.15);
    }
    .label {
        font-size: 0.98rem;
        color: #444;
        text-align: center;
        margin-top: 0.1rem;
        font-weight: 500;
        min-width: 90px;
        max-width: 120px;
        line-height: 1.2;
    }
    .bar {
        position: absolute;
        top: 18px;
        left: 50%;
        width: 100%;
        height: 4px;
        background: #e0e7ef;
        z-index: 1;
    }
    .step:not(:last-child) .bar {
        right: -50%;
        left: 50%;
        width: 100%;
    }
    .step.completed:not(:last-child) .bar {
        background: linear-gradient(90deg, #27ae60 60%, #667eea 100%);
    }
    .step.active:not(:last-child) .bar {
        background: linear-gradient(90deg, #764ba2 60%, #667eea 100%);
    }
    @media (max-width: 900px) {
        .label { font-size: 0.85rem; min-width: 60px; max-width: 90px; }
        .circle { width: 30px; height: 30px; font-size: 1rem; }
    }
    @media (max-width: 600px) {
        .stepper-container { flex-direction: column; align-items: flex-start; }
        .step { flex-direction: row; margin-bottom: 1.2rem; }
        .label { margin-left: 0.7rem; margin-top: 0; text-align: left; }
        .bar { display: none; }
    }
    </style>
    <div class="stepper-container">
    """
    for i, label in enumerate(steps, 1):
        status = ""
        if current > i:
            status = "completed"
        elif current == i:
            status = "active"
        stepper_html += f"<div class='step {status}'>"
        stepper_html += f"<div class='circle'>{i}</div>"
        if i < len(steps):
            stepper_html += f"<div class='bar'></div>"
        stepper_html += f"<div class='label'>{label}</div>"
        stepper_html += "</div>"
    stepper_html += "</div>"
    st.markdown(stepper_html, unsafe_allow_html=True)
    if st.button("🔄 Start Over"):
        # Only reset workflow-related keys
        for k in [
            'step', 'detail_image', 'detail_image_bytes', 'detail_image_preview',
            'extracted_text', 'extracted_text_confirmed', 'requirements',
            'product_image', 'product_image_bytes', 'product_image_preview',
            'generated_poster_bytes', 'generated_poster_versions',
            'improvement_prompt', 'upload_result', 'regenerating',
            'regeneration_prompts', 'error'
        ]:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state["step"] = 1
        st.experimental_rerun()

    st.title("🎨 AI Poster Generator")

    # --- Step 1: Upload Product Detail Image ---
    if st.session_state.step == 1:
        st.header("Step 1: Upload Product Detail Image")
        uploaded = st.file_uploader(
            "Upload a product detail image (JPG, PNG, JPEG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="detail_image_uploader"
        )
        if uploaded:
            st.session_state.detail_image = uploaded
            st.session_state.detail_image_bytes = uploaded.read()
            st.session_state.detail_image_preview = base64.b64encode(st.session_state.detail_image_bytes).decode()
            st.image(bytes_to_image(st.session_state.detail_image_bytes), caption="Product Detail Image Preview", use_column_width=True)
            if st.button("Extract Text", key="extract_text_btn"):
                with st.spinner("Extracting text from image..."):
                    try:
                        text = extract_text_from_image_api(st.session_state.detail_image_bytes)
                        st.session_state.extracted_text = text
                        st.session_state.step = 2
                        st.session_state.error = ''
                        st.experimental_rerun()
                    except Exception as e:
                        st.session_state.error = f"Error extracting text: {str(e)}"
        if st.session_state.error:
            st.error(st.session_state.error)

    # --- Step 2: Display Extracted Text ---
    elif st.session_state.step == 2:
        st.header("Step 2: Display Extracted Text")
        st.success("Text extracted successfully!")
        st.session_state.extracted_text = st.text_area(
            "Extracted Text (edit if needed)",
            value=st.session_state.extracted_text or '',
            height=120,
            key="extracted_text_area"
        )
        if st.button("Confirm Text", key="confirm_text_btn"):
            if st.session_state.extracted_text and st.session_state.extracted_text.strip():
                st.session_state.extracted_text_confirmed = True
                st.session_state.step = 3
                st.session_state.error = ''
                st.experimental_rerun()
            else:
                st.session_state.error = "Extracted text cannot be empty."
        if st.session_state.error:
            st.error(st.session_state.error)

    # --- Step 3: Requirements Input ---
    elif st.session_state.step == 3:
        st.header("Step 3: Poster Requirements")
        st.session_state.requirements = st.text_area(
            "Describe what kind of poster you want to create...",
            value=st.session_state.requirements or '',
            max_chars=500,
            height=120,
            key="requirements_area"
        )
        req_len = len(st.session_state.requirements) if st.session_state.requirements else 0
        st.caption(f"{req_len}/500 characters")
        with st.expander("💡 Example Prompts"):
            st.markdown("""
            - Create a festive promotional poster for a Diwali sale.
            - Design a modern social media post for Instagram.
            - Make an eye-catching advertisement for a new product launch.
            - Highlight product features for a WhatsApp campaign.
            """)
        if st.button("Next: Upload Product Photo", key="to_product_photo"):
            if st.session_state.requirements and st.session_state.requirements.strip():
                st.session_state.step = 4
                st.session_state.error = ''
                st.experimental_rerun()
            else:
                st.session_state.error = "Please describe your poster requirements."
        if st.session_state.error:
            st.error(st.session_state.error)

    # --- Step 4: Upload Product Photo ---
    elif st.session_state.step == 4:
        st.header("Step 4: Upload Product Photo")
        # Only show the uploader and preview for the product photo
        uploaded2 = st.file_uploader(
            "Upload the actual product photo (JPG, PNG, JPEG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="product_image_uploader"
        )
        if uploaded2:
            st.session_state.product_image = uploaded2
            st.session_state.product_image_bytes = uploaded2.read()
            st.session_state.product_image_preview = base64.b64encode(st.session_state.product_image_bytes).decode()
            st.image(bytes_to_image(st.session_state.product_image_bytes), caption="Product Photo Preview", use_column_width=True)
        if st.session_state.product_image_bytes:
            if st.button("Next: Generate Poster", key="to_generate_poster"):
                st.session_state.step = 5
                st.session_state.error = ''
                st.experimental_rerun()
        if st.session_state.error:
            st.error(st.session_state.error)

    # --- Step 5: Generate Poster ---
    elif st.session_state.step == 5:
        st.header("Step 5: Generate Poster")
        st.subheader("Summary of Inputs")
        st.markdown(f"**Extracted Text:** {st.session_state.extracted_text}")
        st.markdown(f"**Requirements:** {st.session_state.requirements}")
        # Only show the product photo preview
        if st.session_state.product_image_bytes:
            st.image(bytes_to_image(st.session_state.product_image_bytes), caption="Product Photo", use_column_width=True)
        if st.button("Generate Poster", key="generate_poster_btn"):
            with st.spinner("Generating poster with AI..."):
                try:
                    poster_bytes = generate_poster_api(
                        st.session_state.product_image_bytes,
                        st.session_state.extracted_text,
                        st.session_state.requirements
                    )
                    st.session_state.generated_poster_bytes = poster_bytes
                    st.session_state.generated_poster_versions.append(poster_bytes)
                    st.session_state.step = 6
                    st.session_state.error = ''
                    st.experimental_rerun()
                except Exception as e:
                    st.session_state.error = f"Error generating poster: {str(e)}"
        if st.session_state.error:
            st.error(st.session_state.error)

    # --- Step 6: Review and Action ---
    elif st.session_state.step == 6:
        st.header("Step 6: Review and Action")
        if st.session_state.generated_poster_bytes:
            st.image(bytes_to_image(st.session_state.generated_poster_bytes), caption="Generated Poster", use_column_width=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Upload to Drive", key="upload_to_drive_btn"):
                    with st.spinner("Uploading to Google Drive..."):
                        # Detect file type for mimetype
                        poster_bytes = st.session_state.generated_poster_bytes
                        # Default to PNG
                        mimetype = 'image/png'
                        if poster_bytes[:3] == b'\xff\xd8\xff':
                            mimetype = 'image/jpeg'
                        # Use correct mimetype in upload
                        try:
                            result = DriveHandler.upload_to_drive(poster_bytes, "generated_images", "generated_poster.png")
                            st.session_state.upload_result = result
                            # Show raw result for debugging
                            if result and result.get("success", True):
                                st.success("Poster uploaded to Google Drive successfully!")
                                if st.button("Generate Another Poster", key="generate_another"):
                                    for k in list(st.session_state.keys()):
                                        del st.session_state[k]
                                    st.experimental_rerun()
                            else:
                                st.error(f"Upload failed: {result.get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Exception during upload: {str(e)}")
            with col2:
                if st.button("🔄 Regenerate with Improvements", key="regenerate_btn"):
                    st.session_state.regenerating = True
                    st.session_state.error = ''
                    st.experimental_rerun()
            if st.session_state.regenerating:
                st.markdown("---")
                st.subheader("Regenerate Poster with Improvements")
                st.session_state.improvement_prompt = st.text_area(
                    "Describe what you want to improve (e.g., change colors, adjust layout, fix text, modify style...)",
                    value=st.session_state.improvement_prompt or '',
                    height=100,
                    key="improvement_prompt_area"
                )
                st.markdown(f"**Original Requirements:** {st.session_state.requirements}")
                if st.button("Generate Improved Poster", key="generate_improved_btn"):
                    if st.session_state.improvement_prompt and st.session_state.improvement_prompt.strip():
                        with st.spinner("Regenerating poster with improvements..."):
                            try:
                                improved_bytes = regenerate_poster_api(
                                    st.session_state.product_image_bytes,
                                    st.session_state.extracted_text,
                                    st.session_state.requirements,
                                    st.session_state.improvement_prompt or ''
                                )
                                st.session_state.generated_poster_bytes = improved_bytes
                                st.session_state.generated_poster_versions.append(improved_bytes)
                                st.session_state.improvement_prompt = ''
                                st.session_state.regenerating = False
                                st.session_state.error = ''
                                st.experimental_rerun()
                            except Exception as e:
                                st.session_state.error = f"Error regenerating poster: {str(e)}"
                    else:
                        st.session_state.error = "Please describe what you want to improve."
            st.markdown("---")
            st.download_button(
                label="⬇️ Download Poster",
                data=st.session_state.generated_poster_bytes,
                file_name="generated_poster.png",
                mime="image/png"
            )
            st.markdown("---")
            st.subheader("All Generated Versions")
            for i, poster in enumerate(st.session_state.generated_poster_versions, 1):
                st.image(bytes_to_image(poster), caption=f"Version {i}", use_column_width=True)
        if st.session_state.error:
            st.error(st.session_state.error) 