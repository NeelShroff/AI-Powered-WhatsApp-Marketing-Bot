from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import base64
import os
from pathlib import Path

load_dotenv()

# Initialize the OpenAI chat model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

def get_image_mime_type(image_path):
    """Get MIME type based on file extension"""
    extension = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.tiff': 'image/tiff',
        '.tif': 'image/tiff'
    }
    return mime_types.get(extension, 'image/jpeg')  # Default to jpeg if unknown

def encode_image(image_path):
    """Encode image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Error reading image file: {str(e)}")

def extract_text_from_image(image_path):
    """Extract text from image using LangChain and OpenAI"""
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return f"Error: Image file '{image_path}' not found."
        
        # Get the correct MIME type
        mime_type = get_image_mime_type(image_path)
        
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Create message with image
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Extract all the text from this image. Please provide the text exactly as it appears in the image."},
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
            ]
        )
        
        # Get response from OpenAI
        response = llm.invoke([message])
        
        return response.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def is_supported_image_format(image_path):
    """Check if the image format is supported"""
    supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    extension = Path(image_path).suffix.lower()
    return extension in supported_extensions

# Usage
if __name__ == "__main__":
    image_path = "test4.jpg"  # Update with your image path
    
    # Check if the image format is supported
    if not is_supported_image_format(image_path):
        print(f"Warning: Image format may not be supported. Supported formats: JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF")
    
    extracted_text = extract_text_from_image(image_path)
    
    print("Extracted Text:")
    print(extracted_text)