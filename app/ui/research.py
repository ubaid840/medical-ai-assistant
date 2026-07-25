import streamlit as st

def render_research():
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #fef08a, #fde047); color: #854d0e; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>🔬</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Clinical Trial & Research Agent</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Search live medical databases and web resources for the latest trials.</p>
        </div>
    """, unsafe_allow_html=True)
    
    query = st.text_input("Enter a disease or condition (e.g. 'Advanced Melanoma')", placeholder="e.g. Type 2 Diabetes clinical trials")
    
    if st.button("Search Medical Literature", type="primary"):
        if not query:
            st.warning("Please enter a query.")
            return
            
        with st.spinner("Agent is searching the web..."):
            try:
                from duckduckgo_search import DDGS
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
