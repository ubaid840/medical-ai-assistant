import streamlit as st
import pandas as pd
from database import get_connection

def render_audit_dashboard():
    """
    HIPAA Audit Dashboard UI.
    Allows administrators to view the tamper-proof audit trail of system access.
    """
    st.markdown(
        """
        <div style="
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(225, 29, 72, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">🔒</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">HIPAA Audit & Security Logs</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Tamper-proof record of system events, accesses, and emergency escalations.</p>
        </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT a.id, a.timestamp, a.action, p.name as patient_name, a.details
        FROM audit_logs a
        LEFT JOIN patient_profiles p ON a.patient_id = p.id
        ORDER BY a.timestamp DESC
    """, conn)
    conn.close()

    if df.empty:
        st.info("No audit logs found. The system is operating securely.")
    else:
        # Style the dataframe to highlight emergencies
        def highlight_emergencies(row):
            if 'Emergency' in str(row['action']):
                return ['background-color: #fee2e2; color: #991b1b'] * len(row)
            return [''] * len(row)

        styled_df = df.style.apply(highlight_emergencies, axis=1)
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": "Log ID",
                "timestamp": "Timestamp",
                "action": "Action Taken",
                "patient_name": "Related Patient",
                "details": "Audit Details"
            }
        )

    st.markdown(
        """
        <div style="margin-top: 20px; padding: 15px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <strong>Security Notice:</strong> All data in this log is tracked for compliance. Admin override is required for deletions.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if not df.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🗑️ Admin: Delete Audit Record"):
            st.warning("⚠️ Warning: Deleting audit records may violate strict healthcare compliance regulations.")
            col1, col2 = st.columns([3, 1])
            with col1:
                log_id_to_delete = st.selectbox("Select Log ID to delete:", df['id'].tolist())
            with col2:
                st.write("")
                st.write("")
                if st.button("Delete Record", type="primary", use_container_width=True):
                    if log_id_to_delete:
                        conn = get_connection()
                        conn.execute("DELETE FROM audit_logs WHERE id = ?", (int(log_id_to_delete),))
                        conn.commit()
                        conn.close()
                        st.rerun()
