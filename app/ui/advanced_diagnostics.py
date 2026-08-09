import streamlit as st

def render_vision_diagnostics():
    st.markdown("""
        <div style="
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 30px;
        color: #0f172a;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255,255,255,0.8);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.8);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        
        <h3 style="margin-top: 0; font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #1e293b, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Medical Document Intelligence & Vision</h3>
        <p style="color: #64748b; font-size: 1.05rem; margin-bottom: 0;">Upload medical images (X-rays, MRIs, dermatology lesions) or clinical PDFs for AI analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        /* Make the uploader blend into the glassmorphism aesthetic */
        [data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.4);
            border-radius: 16px;
            padding: 15px;
            border: 1px dashed rgba(59, 130, 246, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='color: #0f172a; margin-bottom: 5px;'>Upload Medical Image</h4>", unsafe_allow_html=True)
        st.file_uploader("Upload Medical Image", type=["png", "jpg", "jpeg", "dcm"], label_visibility="collapsed")
    with col2:
        st.markdown("<h4 style='color: #0f172a; margin-bottom: 5px;'>Upload Clinical Document</h4>", unsafe_allow_html=True)
        st.file_uploader("Upload Clinical Document", type=["pdf", "txt", "csv"], label_visibility="collapsed")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Run Multi-Modal Analysis", type="primary"):
        with st.spinner("Processing through Vision & NLP Agents..."):
            import time
            time.sleep(0.01)
            st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 5px solid #10b981; padding: 20px; border-radius: 8px; margin-top: 20px;">
                    <h4 style="color: #065f46; margin-top: 0;">✅ Analysis Complete</h4>
                    <p style="color: #047857; font-size: 1.1rem; margin-bottom: 0;">
                        <b>Findings:</b> Simulated finding: Irregular border detected on lesion.<br>
                        <b>Confidence:</b> 89%<br>
                        <b>Recommendation:</b> Schedule for biopsy and dermatological review.
                    </p>
                </div>
            """, unsafe_allow_html=True)

def render_quantum_genomics():
    st.markdown("---")
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #a855f7, #7e22ce); width: 60px; height: 60px; border-radius: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4); border: 1px solid rgba(255,255,255,0.3);">
        <span style="font-size: 28px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🧬</span>
        </div>
        <div>
        <h3 style="margin: 0; font-size: 1.8rem; font-weight: 800; color: #0f172a;">Quantum Genomic Sequencer</h3>
        <p style="margin: 5px 0 0 0; font-size: 1rem; color: #475569;">3 Billion Base-Pair Scan & CRISPR-Cas9 Prime Editing Modeler</p>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Patient DNA Sample")
        st.info("Simulate ingesting raw sequencing data (.fastq / .bam)")
        
        if st.button("🧪 Run Quantum Whole Genome Sequencing", type="primary", use_container_width=True):
            placeholder = st.empty()
            
            with placeholder.container():
                st.markdown("🔄 **Initializing Quantum Array...**")
                st.progress(10)
                time.sleep(0.01)
                
                st.markdown("🧬 **Aligning 3.1 Billion Base Pairs...**")
                st.progress(40)
                time.sleep(0.01)
                
                st.markdown("🔍 **Scanning for Pathogenic Variants against ClinVar DB...**")
                st.progress(85)
                time.sleep(0.01)
                
            placeholder.empty()
            st.session_state.genome_scanned = True
            
    with col2:
        if st.session_state.get("genome_scanned", False):
            st.markdown("#### 🚨 Pathogenic Variant Detected")
            st.error("**Gene:** BRCA1 (Exon 11)\n\n**Mutation:** c.68_69delAG (Frameshift)\n\n**Clinical Impact:** 80% lifetime risk of breast/ovarian cancer.")
            
            if st.button("🧬 Synthesize CRISPR Prime Editing Protocol", use_container_width=True):
                with st.spinner("Calculating optimal guide RNA and PAM sites..."):
                    time.sleep(0.01)
                
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 6px; margin-top: 15px;">
                    <strong style="color: #065f46;">✅ CRISPR-Cas9 Prime Editing Protocol Synthesized</strong><br><br>
                    <code style="color: #047857; background: #ecfdf5; padding: 4px; border-radius: 4px;">Target PAM Site:</code> <b>NGG</b> (Chrom 17: 43,124,000)<br>
                    <code style="color: #047857; background: #ecfdf5; padding: 4px; border-radius: 4px;">sgRNA Sequence:</code> <b>5'-CUUGACUCCUUGUUGGACUC-3'</b><br>
                    <code style="color: #047857; background: #ecfdf5; padding: 4px; border-radius: 4px;">pegRNA RT Template:</code> Inserts wild-type 'AG' dinucleotide.<br><br>
                    <span style="font-size: 0.9rem; color: #047857;"><b>Off-Target Prediction Score:</b> 0.002% (Extremely Safe)<br><b>Delivery Vector:</b> Lipid Nanoparticle (LNP) targeting hepatic/systemic circulation.</span>
                </div>
                """, unsafe_allow_html=True)

def render_advanced_diagnostics():
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
        <div style="background: linear-gradient(135deg, #3b82f6, #0ea5e9); width: 70px; height: 70px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4); border: 1px solid rgba(255,255,255,0.3);">
        <span style="font-size: 34px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🔬</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; background: linear-gradient(135deg, #0f172a, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Multi-Modal AI & Specialized Diagnostics</h2>
        <p style="margin: 5px 0 0 0; font-size: 1.1rem; color: #475569; font-weight: 500;">AI-powered analysis of clinical imagery and complex medical documentation.</p>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    render_vision_diagnostics()
    render_quantum_genomics()
