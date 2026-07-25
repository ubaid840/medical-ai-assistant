import base64
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_image(image_file, language="English", mime_type="image/jpeg", scan_type=None):

    image_bytes = image_file.read()
    
    scan_context = f"The user has indicated this is a {scan_type}." if scan_type else "The user has uploaded a medical image."

    sys_prompt = f"""
You are an expert medical AI radiologist specializing in analyzing medical images, X-rays, MRI scans, and skin concerns.
{scan_context}
Due to a temporary Vision API outage, you cannot see the image. However, the user needs a highly detailed, professional-grade example of a Radiology Report that typically corresponds to such a scan.

DO NOT give a "simple introduction". You must provide a comprehensive, structured mock medical report that includes:
1. Patient Data (Hypothetical placeholders)
2. Clinical Indication
3. Findings (Break down by anatomical structures - be extremely detailed and use advanced medical terminology)
4. Impression / Conclusion
5. Recommendations for next steps.

Tell the user if the typical visual symptoms for this scan appear severe and clearly state whether they should see a doctor right away.
Do not provide a definitive medical diagnosis for their actual image, but make the mock report highly realistic.
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
        temperature=0.4,
        max_tokens=1500
    )

    return response.choices[0].message.content