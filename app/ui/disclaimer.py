import streamlit as st


def show_disclaimer():
    st.info(
        """
### ⚠ Medical Disclaimer

This Medical AI Platform is intended **only for educational and informational purposes** using uploaded medical documents.

**Important:**

- It does **NOT** replace a licensed healthcare professional.
- It does **NOT** provide medical diagnosis.
- It does **NOT** prescribe medications.
- AI responses may contain errors or incomplete information.
- Always verify medical information with qualified healthcare providers.

🚨 **If you are experiencing a medical emergency, contact your local emergency services or visit the nearest hospital immediately.**
"""
    )