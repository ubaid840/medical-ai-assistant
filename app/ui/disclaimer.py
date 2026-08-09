import streamlit as st


def show_disclaimer():
    html_disclaimer = """
    <div style="background: linear-gradient(145deg, #f0f9ff, #e0f2fe); border-left: 5px solid #0284c7; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(2, 132, 199, 0.1); margin-bottom: 2rem; font-family: 'Inter', sans-serif;">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: #0ea5e9; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-right: 12px; box-shadow: 0 2px 10px rgba(14, 165, 233, 0.3);">
                ⚠️
            </div>
            <h3 style="margin: 0; color: #0369a1; font-weight: 700; font-size: 1.3rem; letter-spacing: -0.5px;">Medical Disclaimer</h3>
        </div>
        <p style="color: #0f172a; font-size: 1rem; line-height: 1.6; margin-bottom: 1.2rem;">
            This Medical AI Platform is intended <strong style="color: #0284c7; background: rgba(2, 132, 199, 0.1); padding: 2px 6px; border-radius: 4px;">only for educational and informational purposes</strong> using uploaded medical documents.
        </p>
        <div style="background: rgba(255, 255, 255, 0.7); padding: 1.2rem; border-radius: 8px; border: 1px solid rgba(14, 165, 233, 0.2);">
            <strong style="color: #075985; display: block; margin-bottom: 10px; font-size: 1.05rem;">Critical Reminders:</strong>
            <ul style="margin: 0; padding-left: 1.5rem; font-size: 0.95rem; line-height: 1.7; color: #334155;">
                <li>It does <strong style="color: #b91c1c;">NOT</strong> replace a licensed healthcare professional.</li>
                <li>It does <strong style="color: #b91c1c;">NOT</strong> provide medical diagnosis or prescribe medications.</li>
                <li>AI responses may contain errors, hallucinations, or incomplete information.</li>
                <li>Always verify medical information with qualified healthcare providers.</li>
            </ul>
        </div>
        <div style="margin-top: 1.2rem; padding: 1rem; background: linear-gradient(to right, #fef2f2, #fff1f2); border-left: 4px solid #ef4444; border-radius: 6px; color: #991b1b; font-size: 0.95rem; font-weight: 600; display: flex; align-items: flex-start; box-shadow: inset 0 0 10px rgba(239, 68, 68, 0.05);">
            <span style="font-size: 1.2rem; margin-right: 12px; margin-top: 2px;">🚨</span>
            <div style="line-height: 1.5;">
                If you are experiencing a medical emergency, contact your local emergency services or visit the nearest hospital immediately.
            </div>
        </div>
    </div>
    """
    st.markdown(html_disclaimer, unsafe_allow_html=True)
