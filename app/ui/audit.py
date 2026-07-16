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
        <div class="card">
        <h3 style="display: flex; align-items: center; gap: 10px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            HIPAA Audit & Security Logs
        </h3>
        <p style="color: #64748b; font-size: 0.95rem;">Tamper-proof record of system events, accesses, and emergency escalations.</p>
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
