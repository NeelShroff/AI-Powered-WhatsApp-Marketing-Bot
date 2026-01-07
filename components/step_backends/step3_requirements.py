def get_prompt_by_category(category):
    """
    Get the full prompt text for a specific category from promptselection.txt
    Args:
        category (str): The category name (e.g., 'Health & Wellness', 'Premium Luxury', etc.)
    Returns:
        str: The full prompt text for that category
    """
    import os
    import re
    
    # Map category names to their numbers in the file
    category_map = {
        'Health & Wellness': '1',
        'Eco-Friendly': '2', 
        'Technology-Focused': '3',
        'Family-Oriented': '4',
        'Premium Luxury': '5'
    }
    
    if category not in category_map:
        return f"Category '{category}' not found"
    
    try:
        # Get the path to promptselection.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(current_dir, '..', '..', 'backend', 'promptselection.txt')
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        # Normalize newlines for consistent regex behavior
        content = raw.replace('\r\n', '\n').replace('\r', '\n')

        # Number tag for the requested category
        num = category_map[category]

        # Regex: match a line containing just the number, capture everything until the next numbered line (1-5) or EOF
        pattern = re.compile(
            rf"(?ms)^\s*{re.escape(num)}\s*\n(.*?)(?=^\s*(?:1|2|3|4|5)\s*$|\Z)"
        )
        m = pattern.search(content)
        if not m:
            return f"Prompt for category '{category}' not found"

        section = m.group(1).strip()
        return section
        
    except Exception as e:
        return f"Error reading prompt file: {str(e)}"

def process_requirements(requirements_text):
    """
    Process the poster requirements (e.g., validate, enhance, or send to OpenAI API).
    Args:
        requirements_text (str): The requirements input by the user.
    Returns:
        Any: Result of processing (to be defined by your OpenAI API logic).
    """
    # TODO: Implement OpenAI API call here
    return requirements_text

def get_available_categories():
    """
    Get list of available prompt categories
    Returns:
        list: List of category names
    """
    return [
        'Health & Wellness',
        'Eco-Friendly', 
        'Technology-Focused',
        'Family-Oriented',
        'Premium Luxury'
    ]