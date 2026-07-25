import streamlit as st

def render_pediatrics():
    st.header("👶 Pediatrics Care")
    st.markdown("Dedicated interface for managing pediatric patients, monitoring growth charts, and accessing child-specific medical information.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Growth Chart")
        st.info("Growth chart visualization (e.g., WHO percentiles) will be displayed here.")
        
    with col2:
        st.subheader("Immunization Schedule")
        st.success("Recommended immunization tracking for the selected pediatric patient.")

    st.divider()
    st.markdown("### Pediatric Dosing Calculator")
    st.warning("Please consult the Pharmacology tab or chat with the Pediatrics Agent for specific medication dosing.")
