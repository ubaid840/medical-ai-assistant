import base64
from groq import Groq

from config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def analyze_medical_image(image_file, language="English", mime_type="image/jpeg"):

    image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    sys_prompt = f"""
You are a medical AI assistant specializing in analyzing images of rashes, cuts, skin spots, and other medical concerns.
Analyze the uploaded image and explain your findings in an educational way.
Tell the user if the visual symptoms appear severe and clearly state whether they should see a doctor right away.
Do not provide a definitive medical diagnosis or prescribe medications.
CRITICAL INSTRUCTION: You must strictly translate and provide your final response entirely in {language}.
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
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