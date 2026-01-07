import tempfile
import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import base64

load_dotenv()

# Initialize the OpenAI chat model with vision capabilities
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    max_tokens=1000
)

def get_image_mime_type_from_bytes(image_bytes):
    """Get MIME type based on image bytes header"""
    if image_bytes.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):
        return 'image/gif'
    elif image_bytes.startswith(b'RIFF') and b'WEBP' in image_bytes[:12]:
        return 'image/webp'
    elif image_bytes.startswith(b'BM'):
        return 'image/bmp'
    else:
        return 'image/jpeg'  # Default fallback

def extract_text_from_image(image_bytes):
    """
    Extract text from the given image using OpenAI API.
    Args:
        image_bytes (bytes): The image file in bytes.
    Returns:
        str: Extracted text.
    """
    try:
        # Validate image bytes
        if not image_bytes or len(image_bytes) == 0:
            return "Error: No image data provided"
        
        # Get the correct MIME type from bytes
        mime_type = get_image_mime_type_from_bytes(image_bytes)
        
        # Encode the image bytes to base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        # Create message with more specific instructions
        message = HumanMessage(
            content=[
                {
                    "type": "text", 
                    "text": "You are an expert OCR system. Extract ALL visible text from this image. Include product names, descriptions, specifications, prices, and any other text you can see. If there is no text visible, say 'No text found in image'. Do not say you cannot process the image."
                },
                {
                    "type": "image_url", 
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
                }
            ]
        )
        
        # Get response from OpenAI with debugging info
        print(f"DEBUG: Image size: {len(image_bytes)} bytes")
        print(f"DEBUG: MIME type detected: {mime_type}")
        print(f"DEBUG: Base64 length: {len(base64_image)}")
        
        response = llm.invoke([message])
        
        print(f"DEBUG: OpenAI response: {response.content}")
        
        # Check if response indicates inability to process
        if "unable to" in response.content.lower() or "cannot" in response.content.lower():
            return f"OpenAI Vision API issue: {response.content}. Please try with a different image or check your OpenAI API key."
        
        return response.content
        
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        return f"Error extracting text: {str(e)}"