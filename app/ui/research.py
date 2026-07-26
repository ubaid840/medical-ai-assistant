import streamlit as st

def render_research():
    st.markdown("""
        <div style="
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 35px 35px;
        color: #0f172a;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255,255,255,0.8);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.8);
        ">
        <div style="position: absolute; top: -100px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        <div style="position: absolute; bottom: -100px; left: 5%; width: 250px; height: 250px; background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: linear-gradient(135deg, #3b82f6, #0284c7); width: 88px; height: 88px; border-radius: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 15px 30px rgba(59,130,246,0.4), inset 0 2px 4px rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.2);">
        <span style="font-size: 42px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2)); color: white;">🔬</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.4rem; font-weight: 900; letter-spacing: -0.5px; background: linear-gradient(135deg, #0f172a, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Clinical Trial & Research Agent</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.15rem; color: #475569; font-weight: 600; letter-spacing: 0.2px;">Search live medical databases and web resources for the latest trials.</p>
        </div>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 10px;">
            <div style="background: linear-gradient(135deg, #60a5fa, #3b82f6); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(59,130,246,0.3);">
                🔍
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Live Literature Search</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Enter a disease, condition, or drug to query clinicaltrials.gov and NCBI.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.form("research_form", border=True):
        query = st.text_input("Research Query", placeholder="e.g. Advanced Melanoma clinical trials and latest treatments")
        submit = st.form_submit_button("🌐 Search Medical Literature", type="primary", use_container_width=True)
        
    if submit:
        if not query.strip():
            st.warning("Please enter a valid research query.")
            return
            
        with st.spinner("Agent is searching the web..."):
            try:
                from ddgs import DDGS
                results = DDGS().text(f"{query} clinical trials latest treatments site:clinicaltrials.gov OR site:ncbi.nlm.nih.gov", max_results=5)
                
                if not results:
                    st.warning("No results found.")
                    return
                
                context = "\n\n".join([f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}" for r in results])
                
                st.markdown("### 🌐 Live Search Results")
                for r in results:
                    st.markdown(f"- **[{r['title']}]({r['href']})**\n  <br><span style='color: gray; font-size: 0.9em;'>{r['body']}</span>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🤖 AI Summary of Findings")
                
                from chatbot import ask_medical_ai
                prompt = f"Act as a Medical Research Assistant. Based ONLY on the following live search results, summarize the latest clinical trials and treatments for '{query}'.\n\nResults:\n{context}"
                
                response = ask_medical_ai(prompt, "research_agent")
                st.write_stream(response.get("answer_generator", ["Error"]))
            except Exception as e:
                st.error(f"Search failed: {e}")
