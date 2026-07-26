import streamlit as st
from config import GROQ_API_KEY
from groq import Groq

def analyze_drug_interactions(medications, patient_context=""):
    client = Groq(api_key=GROQ_API_KEY)
    
    sys_prompt = f"""
You are an expert clinical pharmacologist AI.
The user will provide a list of medications. 
Analyze the potential drug-drug interactions, contraindications, and dietary warnings.
If the user provided patient context, factor their conditions into the analysis.
Format your response in a highly structured, readable format using Markdown.
Use emojis where appropriate. Highlight SEVERE interactions clearly.
Patient Context: {patient_context}
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Please analyze these medications: {', '.join(medications)}"}
        ],
        temperature=0.2,
        max_tokens=1024
    )
    return response.choices[0].message.content


def render_pharmacology():
    """
    Advanced Pharmacology & Drug Interaction Checker UI
    """
    st.markdown(
        """
<div style="
background: linear-gradient(135deg, #10b981 0%, #059669 100%);
border-radius: 20px;
padding: 35px 30px;
color: white;
box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.4);
margin-bottom: 25px;
position: relative;
overflow: hidden;
border: 1px solid rgba(255,255,255,0.2);
">
<div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
<div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

<div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
<div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
<span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">💊</span>
</div>
<div>
<h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Pharmacology Engine</h2>
<p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Advanced drug interaction checker and clinical safety analysis.</p>
</div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 10px;">
            <div style="background: linear-gradient(135deg, #34d399, #10b981); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(16,185,129,0.3);">
                📋
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Clinical Medication Review</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Enter active or prospective medications to run a safety analysis.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Dynamic form for medications
    with st.form("medication_form", border=True):
        med_input = st.text_area(
            "Medications List", 
            placeholder="e.g. Aspirin 81mg, Lisinopril 10mg, Grapefruit Juice...",
            height=120
        )
        
        submit = st.form_submit_button("🧬 Run Comprehensive Interaction Analysis", type="primary", use_container_width=True)
        
        if submit:
            if med_input.strip():
                meds = [m.strip() for m in med_input.replace('\n', ',').split(',') if m.strip()]
                
                if len(meds) > 0:
                    from patient_profile import format_patient_context
                    active_patient_id = st.session_state.get("active_patient_id")
                    patient_context = format_patient_context(active_patient_id) if active_patient_id else "No specific patient context provided."
                    
                    with st.spinner("🧠 Analyzing pharmacological interactions..."):
                        try:
                            analysis_result = analyze_drug_interactions(meds, patient_context)
                            st.session_state.interaction_result = analysis_result
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")
                else:
                    st.warning("Please enter at least one medication.")
            else:
                st.warning("Please enter at least one medication.")
                
    if "interaction_result" in st.session_state:
        st.markdown("---")
        st.markdown("### 🔬 Clinical Interaction Report")
        st.info(st.session_state.interaction_result)
