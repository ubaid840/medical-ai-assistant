import base64
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_image(image_file, language="English", mime_type="image/jpeg", scan_type=None):

    image_bytes = image_file.read()

    # Convert the bytes to base64
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    
    scan_context = f"The user has indicated this is a {scan_type}." if scan_type else ""

    sys_prompt = f"""
You are a highly advanced Medical Vision AI Assistant.
Analyze the following medical image, scan, or physical symptom (e.g., X-ray, MRI, ultrasound, skin lesion).
{scan_context}
1. Provide a detailed, educational analysis of what you observe in the image.
2. Highlight any abnormalities, specific patterns, or areas of concern.
3. If the visual symptoms appear severe (e.g., suspected fracture, severe melanoma, deep wound), clearly state whether the patient should seek immediate medical attention.
4. Always conclude with a disclaimer that you are an AI and this is NOT a definitive medical diagnosis.

CRITICAL INSTRUCTION: You must strictly translate and provide your final response entirely in {language}.
"""

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": sys_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content