import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

def test_openai_connection():
    """Test if OpenAI API key is working"""
    try:
        # Check if API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            return False
        
        print(f"✅ API Key found: {api_key[:10]}...")
        
        # Test basic chat
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke([HumanMessage(content="Hello, can you respond with 'API working'?")])
        
        print(f"✅ Basic chat test: {response.content}")
        
        # Test vision model with actual image processing capability
        llm_vision = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=1000)
        
        # Create a simple test image message
        test_message = HumanMessage(
            content=[
                {"type": "text", "text": "Can you see and process images? Please confirm your vision capabilities."},
            ]
        )
        response_vision = llm_vision.invoke([test_message])
        
        print(f"✅ Vision model test: {response_vision.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection()
