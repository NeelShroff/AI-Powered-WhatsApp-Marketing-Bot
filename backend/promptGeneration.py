import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


class TemplateProcessor:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert AI prompt engineer specializing in creating comprehensive, detailed design prompts for image generation AI. You will receive a design template description and product information. Your task is to merge them into a single, highly detailed and extensive design prompt that leaves no ambiguity about the layout, positioning, colors, typography, spacing, and visual elements. The prompt must be thorough enough that any image generation AI can understand exactly how to create the poster. Use markdown formatting with **bold** text for emphasis. Structure the output as extremely detailed design instructions that specify exact positioning, colors, layout, dimensions, and styling. Integrate the product information into the appropriate sections while keeping the design template structure completely unchanged. The final prompt should be comprehensive and detailed enough to guide precise poster creation."),
            ("user", "DESIGN TEMPLATE:\n{design_template}\n\nPRODUCT INFORMATION:\n{product_information}\n\nINSTRUCTIONS:\n{instructions}\n\nGenerate a single, comprehensive and highly detailed design prompt that covers every aspect of the poster design:")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def process(self, design_template, product_information, instructions):
        try:
            result = self.chain.invoke({
                "design_template": design_template,
                "product_information": product_information,
                "instructions": instructions
            })
            return result
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    processor = TemplateProcessor()
    
    design_template = """
    This vertical portrait poster design features a clean and refreshing aesthetic, built around a white gradient background that gently transitions into a light blue tone toward the middle and bottom. The color scheme emphasizes clarity and balance, using blue for key highlights and emphasis, green to suggest eco-friendliness and nature, orange sparingly for branding elements, and grey subtly for secondary information. At the top of the poster, the company logo is positioned in the top-left corner on a white background, appearing multi-colored and minimalistic. On the top-right corner, there is a rounded badge or sticker-style shape that contains branding or origin-related information. Both upper corners feature green leafy vector decorations which is litten bit transprent , partially overlapping the badge, which reinforce the organic and natural theme of the design. The middle section serves as the main content block. Here, text elements are center-aligned and vertically stacked, with consistent spacing between them. Each block alternates between blue, green, and grey to emphasize different types of information. Fine lines are used to separate the blocks, improving visual clarity. Numerical or metric values are displayed in bold blue for immediate emphasis, while supportive descriptive text is rendered in softer grey or green tones to maintain visual harmony. On the right side of the poster, a tall, white-colored generic product is vertically aligned. It stands out as a visual focal point, enhanced by a realistic water splash effect at its base. This splash grounds the product and creates the impression that it is emerging from water — conveying purity, freshness, and quality. The bottom section of the poster ties everything together. A campaign hashtag is placed in the bottom-left corner, while a disclaimer is set within a full-width green bar across the bottom, using white text in a clean sans-serif font. The website URL or call-to-action is prominently displayed in bold black on the bottom-right, ensuring visibility and access.
    """
    
    product_info = """
        CTO FILTER  
    Carbon Block Fillter

    Absorb toxic substances like
    pestcide, chlorine, substance
    larger than 5 micron, improves taste

    Maximum operating pressure 125psi

    Operating Temperature 4-42℃.

    Life time: 6 months

    Applications in RO water purifier
    (before RO membrane)
    """
    
    instructions = """
    Generate a SINGLE, highly comprehensive and extensively detailed design prompt by combining the DESIGN TEMPLATE with the PRODUCT INFORMATION provided above. This prompt will be used for image generation when provided with actual product and logo images. The prompt must be detailed enough that any AI can understand exactly how to create the poster without any ambiguity.

    STRUCTURE THE PROMPT WITH EXTENSIVE DETAIL:
    1. Start with: "Design a **vertical portrait poster** with a clean and refreshing aesthetic..."
    2. Use **bold markdown formatting** extensively for key terms, sections, colors, and positioning throughout
    3. Expand on every design element from the DESIGN TEMPLATE - include specific details about:
       - Exact positioning and alignment of every element
       - Detailed color specifications and where each color should be used
       - Typography details (font weights, sizes, styling)
       - Spacing and padding between elements
       - Background gradients and transitions
       - Visual effects and styling
    4. Keep the DESIGN TEMPLATE structure EXACTLY as written - do not change any layout, positioning, colors, or design elements
    5. Replace generic product references with the specific product name and details from the PRODUCT INFORMATION section
    6. Insert the product specifications from the PRODUCT INFORMATION as a detailed, well-formatted list with clear hierarchy
    7. Include all contact information and branding details from the PRODUCT INFORMATION with specific formatting instructions
    8. Describe the visual hierarchy and flow of the poster in detail
    9. End with: "**Once I provide both the actual product image and the company logo**, the AI must generate the final poster based on the above layout, integrating the provided images into their specified positions and preserving the complete structure, aesthetics, and formatting described."

    MAKE THE PROMPT EXTREMELY COMPREHENSIVE:
    - Create ONE SINGLE, EXTENSIVE PROMPT that leaves no room for misinterpretation
    - Use ONLY the DESIGN TEMPLATE and PRODUCT INFORMATION provided above
    - Expand every design element into detailed specifications
    - Include specific instructions for text formatting, colors, positioning, and spacing
    - Make it thorough enough that any image generation AI can create the exact poster you want
    - The prompt should be long and detailed enough to guide precise poster creation
    - Do not add marketing language beyond what is in the PRODUCT INFORMATION
    """
    
    result = processor.process(design_template, product_info, instructions)
    print(result)

if __name__ == "__main__":
    main()