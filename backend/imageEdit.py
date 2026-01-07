# Import the packages
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import time
import tempfile

# Load the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_poster_with_openai(selected_prompt, product_image_bytes, extracted_text, logo_image_bytes=None):
    """
    Generate a poster using OpenAI's image edit API with the selected prompt, product image, and extracted text.
    
    Args:
        selected_prompt (str): The selected prompt from step 3
        product_image_bytes (bytes): The uploaded product image bytes
        extracted_text (str): The extracted text from step 2
        logo_image_bytes (bytes, optional): Company logo image bytes
    
    Returns:
        bytes: Generated poster image bytes
    """
    # Combine the selected prompt with the extracted text
    combined_prompt = f"""{selected_prompt}

**Product Information from Image:**
{extracted_text}

**Additional Instructions:**
- Use the product information above to create accurate and relevant content
- Ensure all text is readable and professionally formatted
- Maintain the style and theme specified in the prompt
- Include contact information: www.hitechro.net, info@hitechro.net, Toll Free: 1800 120 1212
 - Always include the provided company logo (do not replace it) and place it per the layout
"""
    
    # Save product image bytes to temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_file.write(product_image_bytes)
        temp_product_path = temp_file.name
    
    try:
        # Prepare images list
        images_to_edit = [open(temp_product_path, "rb")]

        # If no logo bytes provided, attempt to load default logo from backend/image.png
        if logo_image_bytes is None:
            try:
                default_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image.png')
                if os.path.exists(default_logo_path):
                    with open(default_logo_path, 'rb') as lf:
                        logo_image_bytes = lf.read()
            except Exception:
                # Fail silently if default logo not found or unreadable
                pass

        # Add logo if available
        if logo_image_bytes:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_logo:
                temp_logo.write(logo_image_bytes)
                temp_logo_path = temp_logo.name
            images_to_edit.append(open(temp_logo_path, "rb"))
        
        # Generate poster using OpenAI
        img = client.images.edit(
            model="gpt-image-1",
            image=images_to_edit,
            prompt=combined_prompt,
            size="1024x1536",
            n=1,
            quality="high",
            output_format="png",
        )
        
        # Close file handles
        for img_file in images_to_edit:
            img_file.close()
        
        # Convert response to bytes
        image_bytes = base64.b64decode(img.data[0].b64_json)
        return image_bytes
        
    except Exception as e:
        print(f"Error generating poster: {str(e)}")
        raise e
    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_product_path)
            if logo_image_bytes and 'temp_logo_path' in locals():
                os.unlink(temp_logo_path)
        except:
            pass

def save_generated_poster(image_bytes, filename=None):
    """
    Save the generated poster to a file.
    
    Args:
        image_bytes (bytes): The generated poster image bytes
        filename (str, optional): Custom filename, defaults to timestamp-based name
    
    Returns:
        str: Path to the saved file
    """
    if not filename:
        filename = f"generated_poster_{int(time.time())}.png"
    
    with open(filename, "wb") as f:
        f.write(image_bytes)
    
    return filename

# Example usage (commented out for library use)
# if __name__ == "__main__":
#     # Example parameters
#     sample_prompt = "Create a modern poster..."
#     sample_text = "Product details..."
#     
#     with open("product_image.jpg", "rb") as f:
#         product_bytes = f.read()
#     
#     poster_bytes = generate_poster_with_openai(sample_prompt, product_bytes, sample_text)
#     saved_path = save_generated_poster(poster_bytes)
#     print(f"Poster saved to: {saved_path}")