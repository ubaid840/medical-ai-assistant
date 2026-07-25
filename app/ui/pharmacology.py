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
background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
border-radius: 24px;
padding: 40px 35px;
color: white;
box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.6);
margin-bottom: 30px;
position: relative;
overflow: hidden;
border: 1px solid rgba(255,255,255,0.1);
">
<div style="position: absolute; top: -50px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; filter: blur(20px); pointer-events: none;"></div>
<div style="position: absolute; bottom: -80px; left: 5%; width: 200px; height: 200px; background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; filter: blur(20px); pointer-events: none;"></div>

<div style="display: flex; align-items: center; gap: 30px; position: relative; z-index: 1;">
<div style="background: linear-gradient(135deg, rgba(14,165,233,0.2), rgba(99,102,241,0.2)); backdrop-filter: blur(12px); width: 85px; height: 85px; border-radius: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.15);">
<span style="font-size: 42px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">💊</span>
</div>
<div>
<h2 style="margin: 0; font-size: 2.4rem; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(to right, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Pharmacology Engine</h2>
<p style="margin: 10px 0 0 0; font-size: 1.15rem; color: #94a3b8; font-weight: 400; letter-spacing: 0.3px;">Advanced drug interaction checker and clinical safety analysis.</p>
</div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #e0f2fe, #dbeafe); color: #0284c7; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>🔍</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Scan Medications</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Securely input the medications the patient is currently taking or considering to instantly check for dangerous pharmacological interactions.</p>
        </div>
    """, unsafe_allow_html=True)
    
    def clear_pharma():
        st.session_state.pharma_input_area = ""
        if "interaction_result" in st.session_state:
            del st.session_state.interaction_result

    st.markdown("<h4 style='color: #334155; font-size: 1.1rem; margin-bottom: -40px; font-weight: 600;'>📝 Patient Medication List</h4>", unsafe_allow_html=True)
    med_input = st.text_area(
        "", 
        placeholder="e.g. Aspirin 81mg, Lisinopril, Grapefruit Juice\n\n(Type medications here...)",
        height=160,
        key="pharma_input_area"
    )
    
    col_submit, col_clear = st.columns([0.85, 0.15])
    with col_submit:
        submit = st.button("Analyze Interactions 🧬", use_container_width=True, type="primary")
    with col_clear:
        # Use on_click callback to clear state before the widget re-renders
        st.button("🗑️ Clear", use_container_width=True, key="clear_pharma_input_btn", on_click=clear_pharma)
            
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
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
            else:
                st.warning("Please enter at least one medication.")
        else:
            st.warning("Please enter at least one medication.")
                
    if "interaction_result" in st.session_state:
        st.markdown("<br><hr style='border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
                <div style='background: #0ea5e9; color: white; border-radius: 8px; padding: 6px 10px; font-size: 1.2rem;'>🔬</div>
                <h3 style='margin: 0; color: #0f172a; font-weight: 700;'>Clinical Interaction Report</h3>
            </div>
        """, unsafe_allow_html=True)
        st.info(st.session_state.interaction_result)
