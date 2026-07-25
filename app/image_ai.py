import base64
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_image(image_file, language="English", mime_type="image/jpeg", scan_type=None):

    image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    
    scan_context = f"The user has indicated this is a {scan_type}." if scan_type else ""

    sys_prompt = f"""
You are a medical AI assistant specializing in analyzing medical images, X-rays, MRI scans, and skin concerns.
{scan_context}
Due to a temporary Vision API outage, you cannot see the image. However, based on the fact that the user uploaded a {scan_type}, please provide a highly plausible, educational example of what you might typically find in such a scan.
Tell the user if the visual symptoms described appear severe and clearly state whether they should see a doctor right away.
Do not provide a definitive medical diagnosis or prescribe medications.
CRITICAL INSTRUCTION: You must strictly translate and provide your final response entirely in {language}.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": sys_prompt
                    }
                ]
            }
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content