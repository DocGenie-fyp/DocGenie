import openai
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api.env"))
print("Using dotenv path:", dotenv_path)  # Debugging
load_dotenv(dotenv_path)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Set OPENAI_API_KEY in your environment variables.")

# Initialize OpenAI client correctly
client = OpenAI()  # ✅ Uses API key from env automatically

def generate_medical_report_with_gpt(transcription, role="Specialized Health Assistant"):
    """
    Generates a medical report using OpenAI's GPT.
    """
    try:
        # Define the prompt for generating the report
        prompt = f"""
        You are a {role} generating a well-structured medical report based on the following patient consultation transcript:

        {transcription}

         Please generate a structured medical report with the following sections. Ensure that patient information is presented in a point-by-point format:

         1. **Patient Information** (Provide each detail separately as "Attribute: Value" format, e.g., "Sex: Male", "Blood Pressure: 130/88", etc.)
         2. **Patient Symptoms**
         3. **Diagnosis**
         4. **Recommended Treatment Plan**
         5. **Follow-up Instructions**

        Format the report neatly using bullet points or numbering where appropriate.


        **Strict Formatting Instructions:**  
        - Ensure **proper line breaks** between sections.  
        - Use **bold headings** and bullet points correctly.  
        - Separate sections with **two blank lines** to improve readability.  
        - Ensure a clean, **human-friendly format** that looks like a real report.  
        - If any information is missing, use "N/A" as a placeholder.  
        """

        # Create the chat completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Ensure you are using the correct model
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800  # Increased token limit for better formatting
        )

        # Extract and return the generated report
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error generating medical report with GPT: {e}")
        raise Exception(str(e))
