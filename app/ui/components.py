import streamlit as st

def inject_global_styles():
    st.markdown("""
        <style>
        /* Hide Streamlit Branding completely */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Maximize width and remove padding to feel like a real web app */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1600px !important;
        }
        
        /* Sleek Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b !important;
        }
        [data-testid="stSidebar"] * {
            color: #cbd5e1 !important;
        }
        .stRadio > div {
            gap: 12px;
        }
        .stRadio label {
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            padding: 10px 15px;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        .stRadio label:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Base typography */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_page_header(icon: str, title: str, subtitle: str, color_gradient: str):
    """
    Renders a unified, stunning premium header for any page.
    Example color_gradient: "linear-gradient(135deg, #3b82f6, #0ea5e9)"
    """
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid rgba(0,0,0,0.05);">
        <div style="background: {color_gradient}; width: 70px; height: 70px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2); border: 1px solid rgba(255,255,255,0.2);">
        <span style="font-size: 34px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">{icon}</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; color: #0f172a; letter-spacing: -0.5px;">{title}</h2>
        <p style="margin: 5px 0 0 0; font-size: 1.1rem; color: #64748b; font-weight: 500;">{subtitle}</p>
        </div>
        </div>
    """, unsafe_allow_html=True)
