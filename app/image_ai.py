import base64
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_image(image_file, scan_type="General Medical Image"):

    image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    sys_prompt = f"""
You are a medical AI assistant specializing in analyzing {scan_type}s.
Analyze the uploaded {scan_type} and explain findings in an educational way.
Pay special attention to features typical of a {scan_type}.
Do not provide diagnosis or treatment decisions.
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",

        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this medical image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content