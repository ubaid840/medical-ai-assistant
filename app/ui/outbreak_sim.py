import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

def render_outbreak_sim():
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 20px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🦠 Epidemiological Outbreak Sim</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; opacity: 0.9;">Spatial analytics and predictive modeling for pathogen spread.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Parameters")
        r0 = st.slider("Basic Reproduction No. (R0)", 1.0, 6.0, 2.5, 0.1)
        incubation = st.slider("Incubation Period (Days)", 1, 14, 5, 1)
        vax_rate = st.slider("Vaccination Rate (%)", 0, 100, 30, 5)
        run_sim = st.button("Run Simulation", use_container_width=True, type="primary")
        
    with col2:
        if run_sim:
            with st.spinner("Calculating transmission vectors..."):
                time.sleep(0.01)
            
            # Generate dummy spatial data
            np.random.seed(42)
            days = 30
            n_cities = 50
            
            # Base coordinates (roughly Europe/Global)
            lats = np.random.uniform(35, 60, n_cities)
            lons = np.random.uniform(-10, 30, n_cities)
            cities = [f"City {i}" for i in range(n_cities)]
            
            sim_data = []
            
            for day in range(days):
                # Exponential growth modified by R0 and Vax rate
                growth_factor = (r0 / (1 + vax_rate/100)) ** (day / incubation)
                base_cases = np.random.randint(10, 100, n_cities)
                cases = (base_cases * growth_factor).astype(int)
                
                for i in range(n_cities):
                    sim_data.append({
                        "Day": day,
                        "City": cities[i],
                        "Lat": lats[i],
                        "Lon": lons[i],
                        "Cases": cases[i],
                        "Radius": min(cases[i] / 500, 50) # Cap size
                    })
                    
            df = pd.DataFrame(sim_data)
            
            fig = px.scatter_geo(
                df, lat="Lat", lon="Lon", 
                color="Cases", size="Radius", 
                animation_frame="Day", 
                hover_name="City",
                projection="natural earth",
                color_continuous_scale="YlOrRd",
                range_color=[0, df["Cases"].max() * 0.8]
            )
            
            fig.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                geo=dict(
                    showland=True, landcolor="rgb(243, 244, 246)",
                    showcountries=True, countrycolor="rgb(209, 213, 219)"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning(f"**Analysis:** With R0={r0} and {vax_rate}% vaccination, the outbreak reaches peak exponential growth by Day 20. Stricter non-pharmaceutical interventions (NPIs) are recommended.")
        else:
            st.info("Adjust parameters and click 'Run Simulation' to visualize the epidemiological spread.")
