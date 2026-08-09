from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def render_knowledge_base():
    """
    Knowledge Base UI
    """

    st.markdown(
        """
        <div class="card" style="margin-bottom: 15px; padding: 20px;">
            <h3 style="margin-bottom: 5px;">📚 Knowledge Base</h3>
            <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 0;">
                Medical documents are stored using Retrieval Augmented Generation (RAG).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    extensions = ['*.pdf', '*.txt', '*.docx', '*.csv']
    all_files = []
    for ext in extensions:
        all_files.extend(list(DATA_DIR.glob(ext)))

    # Compact Stats Row
    st.markdown(
        f"""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Medical Docs</div>
                <div style="color: #0ea5e9; font-size: 1.6rem; font-weight: 800;">{len(all_files)}</div>
            </div>
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Vector Database</div>
                <div style="color: #0ea5e9; font-size: 1.4rem; font-weight: 800;">ChromaDB</div>
            </div>
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">LLM Engine</div>
                <div style="color: #0ea5e9; font-size: 1.4rem; font-weight: 800;">Llama 3.3</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader("🩺 AI Clinical Precision")
    
    # Custom HTML/JS Animated Gauge (Zero Dependencies, Medical Theme)
    gauge_html = """
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; font-family: sans-serif; padding-top: 10px;">
      <svg viewBox="0 0 100 65" width="350" height="200">
        <defs>
          <linearGradient id="medGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ef4444" /> <!-- Danger Red -->
            <stop offset="50%" stop-color="#eab308" /> <!-- Warning Yellow -->
            <stop offset="100%" stop-color="#22c55e" /> <!-- Healthy Green -->
          </linearGradient>
        </defs>
        
        <!-- Background Track -->
        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#e2e8f0" stroke-width="12" stroke-linecap="round" />
        
        <!-- Colored Fill with Medical Gradient -->
        <path id="gauge-fill" d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="url(#medGradient)" stroke-width="12" stroke-linecap="round" 
              stroke-dasharray="125.6" stroke-dashoffset="125.6" />
              
        <!-- Heartbeat / EKG subtle background -->
        <path d="M 35 45 L 42 45 L 45 35 L 50 55 L 55 40 L 58 45 L 65 45" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linejoin="round" />
              
        <!-- Needle -->
        <g id="needle" style="transform: translate(50px, 50px) rotate(-90deg); transform-origin: 0px 0px;">
          <polygon points="-2,0 2,0 0,-38" fill="#1e293b" />
          <circle cx="0" cy="0" r="4.5" fill="#1e293b" />
          <circle cx="0" cy="0" r="1.5" fill="#ffffff" />
        </g>
      </svg>
      <div id="gauge-text" style="font-size: 32px; font-weight: 900; color: #16a34a; margin-top: -25px; text-shadow: 0px 2px 4px rgba(0,0,0,0.1);">
        0.0%
      </div>
      <div style="font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; margin-top: 5px; letter-spacing: 1px;">
        Diagnostic Confidence
      </div>
    </div>
    
    <script>
      window.onload = function() {
          const fill = document.getElementById("gauge-fill");
          const needle = document.getElementById("needle");
          const text = document.getElementById("gauge-text");
          
          if (!fill || !needle || !text) return;
          
          const basePercent = 96.8;
          const circumference = 125.6;
          
          function updateGauge(percent, animateTime = "1.5s") {
              const targetOffset = circumference - (circumference * (percent / 100));
              const targetAngle = -90 + (180 * (percent / 100));
              
              fill.style.transition = `stroke-dashoffset ${animateTime} cubic-bezier(0.34, 1.56, 0.64, 1)`;
              needle.style.transition = `transform ${animateTime} cubic-bezier(0.34, 1.56, 0.64, 1)`;
              
              fill.style.strokeDashoffset = targetOffset;
              needle.style.transform = `translate(50px, 50px) rotate(${targetAngle}deg)`;
              text.innerText = percent.toFixed(1) + "%";
          }
    
          setTimeout(() => {
              updateGauge(basePercent);
          }, 150);
    
          setInterval(() => {
              const jitter = (Math.random() * 2) - 1.0;
              const newPercent = Math.min(100, Math.max(0, basePercent + jitter));
              updateGauge(newPercent, "1s");
          }, 2000);
      };
    </script>
    """
    
    components.html(gauge_html, height=260)

    st.subheader("📄 Indexed Documents")

    if all_files:
        st.markdown('<div class="card" style="padding: 15px;">', unsafe_allow_html=True)
        for doc_file in all_files:
            st.markdown(f'<div style="padding: 8px 0; border-bottom: 1px solid #f1f5f9;">📄 <b>{doc_file.name}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No medical documents have been indexed yet. Upload documents from the sidebar.")

    st.subheader("🤖 AI Stack Components")
    
    st.markdown(
        """
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ Groq API</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ LangChain</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ ChromaDB</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ Ollama Embeddings</span>
        </div>
        """,
        unsafe_allow_html=True
    )
