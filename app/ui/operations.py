import streamlit as st
import pandas as pd
from database import get_connection
from datetime import datetime, timedelta

def get_appointments(patient_id=None):
    conn = get_connection()
    if patient_id:
        df = pd.read_sql_query("SELECT id, appointment_date, reason, status, insurance_details FROM appointments WHERE patient_id = ?", conn, params=(patient_id,))
    else:
        df = pd.read_sql_query("SELECT id, patient_id, appointment_date, reason, status FROM appointments", conn)
    conn.close()
    return df

def add_appointment(patient_id, date_str, reason, insurance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_id, appointment_date, reason, insurance_details)
        VALUES (?, ?, ?, ?)
    """, (patient_id, date_str, reason, insurance))
    conn.commit()
    conn.close()

def render_operations():
    st.markdown(
        """
        <div style="
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(6, 182, 212, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">📅</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Patient Management & Operations</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Automated Intake & Scheduling Dashboard</p>
        </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    active_patient_id = st.session_state.get("active_patient_id")
    
    if not active_patient_id:
        st.warning("Please select a patient from the sidebar to view their appointments and intake forms.")
        return
        
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 10px;">
            <div style="background: linear-gradient(135deg, #2dd4bf, #0d9488); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(13,148,136,0.3);">
                📋
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Automated Intake Data</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Patient vitals and clinical history extracted via AI.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # In a real app this would be filled out by AI during chat
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, age, allergies, medications, chronic_conditions FROM patient_profiles WHERE id = ?", (active_patient_id,))
    patient = c.fetchone()
    conn.close()
    
    if patient:
        st.info(f"**Patient:** {patient['name']} (Age: {patient['age']})  \n"
                f"**Known Allergies:** {patient['allergies']}  \n"
                f"**Current Meds:** {patient['medications']}")
    
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 25px;">
            <div style="background: linear-gradient(135deg, #818cf8, #4f46e5); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(79,70,229,0.3);">
                🗓️
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Upcoming Appointments</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Review and manage patient schedule.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    appointments = get_appointments(active_patient_id)
    if not appointments.empty:
        st.dataframe(appointments, use_container_width=True)
    else:
        st.info("No upcoming appointments found. The AI can schedule them automatically via Chat!")
        
    with st.expander("➕ Manually Schedule Appointment"):
        col1, col2 = st.columns(2)
        with col1:
            apt_date = st.date_input("Date")
            apt_time = st.time_input("Time")
        with col2:
            reason = st.text_input("Reason for Visit", placeholder="e.g. Follow-up for hypertension")
            insurance = st.text_input("Insurance Details", placeholder="e.g. BlueCross PPO")
            
        if st.button("Book Appointment"):
            datetime_str = f"{apt_date} {apt_time}"
            add_appointment(active_patient_id, datetime_str, reason, insurance)
            st.success(f"Appointment booked for {datetime_str}!")
            st.rerun()
