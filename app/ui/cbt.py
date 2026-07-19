import streamlit as st
from datetime import datetime
from agents import call_llm

def render_cbt_tab():
    """
    Digital CBT (Cognitive Behavioral Therapy) & Mood Journal UI
    """
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #eef2ff, #ede9fe); padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
            <h2 style="color: #4f46e5; margin-top: 0; display: flex; align-items: center; gap: 10px;">
                🧠 Mental Wellness & Digital CBT
            </h2>
            <p style="color: #475569; font-size: 1.1rem; margin-bottom: 0;">Your judgment-free zone for cognitive behavioral exercises and mood tracking.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
            <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">
                <h3 style="color: #334155; margin-top: 0;">📊 Mood Journal</h3>
            </div>
            """, unsafe_allow_html=True
        )
        st.info("Tracking your daily mood helps the AI adapt its empathy model and provide better support.")
        
        st.write("")
        mood = st.select_slider(
            "How are you feeling today?",
            options=["Awful", "Bad", "Neutral", "Good", "Excellent"],
            value="Neutral"
        )
        st.write("")
        
        journal_entry = st.text_area("Write down your thoughts (optional):", height=100)
        
        if st.button("Save & Analyze Mood", use_container_width=True):
            if journal_entry:
                with st.spinner("AI Therapist is reading your journal..."):
                    prompt = f"You are an empathetic AI Therapist. The patient is feeling '{mood}' today. They wrote in their journal: '{journal_entry}'. Write a short, warm, supportive response (3-4 sentences max) validating their feelings."
                    response = call_llm(prompt, temperature=0.3, max_tokens=200, privacy_mode=st.session_state.get("privacy_mode", False), stream=False)
                    st.success("Mood entry saved!")
                    st.info(f"**AI Therapist:** {response}")
            else:
                st.success("Mood entry saved to your private journal.")
            
    with col2:
        st.markdown(
            """
            <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">
                <h3 style="color: #334155; margin-top: 0;">🧘 Digital CBT Exercises</h3>
            </div>
            """, unsafe_allow_html=True
        )
        st.write("")
        cbt_exercise = st.selectbox(
            "Select an interactive exercise:",
            ["Thought Challenging (ABC Model)", "Box Breathing", "Grounding (5-4-3-2-1)"]
        )
        
        if cbt_exercise == "Thought Challenging (ABC Model)":
            st.markdown(
                """
                <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
                    <strong style="color: #1e293b;">The ABC Model:</strong>
                    <ul style="color: #475569; margin-top: 8px; margin-bottom: 0;">
                        <li><strong>A</strong>ctivating Event: <em>What happened?</em></li>
                        <li><strong>B</strong>elief: <em>What did I tell myself about it?</em></li>
                        <li><strong>C</strong>onsequence: <em>How did it make me feel?</em></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
            event = st.text_area("Activating Event:", placeholder="e.g. I made a small mistake at work...", height=70)
            belief = st.text_area("Belief:", placeholder="e.g. I'm going to get fired...", height=70)
            consequence = st.text_area("Consequence (Emotion):", placeholder="e.g. Extreme anxiety and panic...", height=70)
            
            if st.button("Challenge Thought with AI Therapist"):
                if event and belief and consequence:
                    with st.spinner("AI Therapist is analyzing your thought pattern..."):
                        prompt = f"""You are an expert Cognitive Behavioral Therapist AI. 
The user is doing an ABC thought record.
Activating Event: {event}
Belief: {belief}
Consequence: {consequence}

Identify any cognitive distortions (e.g. catastrophizing, black-and-white thinking) in their belief. Gently challenge this thought and suggest a more balanced, rational alternative perspective in 3-4 sentences."""
                        response = call_llm(prompt, temperature=0.2, max_tokens=300, privacy_mode=st.session_state.get("privacy_mode", False), stream=False)
                        st.info(f"**AI Therapist:** {response}")
                else:
                    st.warning("Please fill out all three fields to challenge the thought.")
                
        elif cbt_exercise == "Box Breathing":
            st.markdown(
                """
                <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e; margin-bottom: 20px;">
                    <strong style="color: #166534;">Box Breathing Technique:</strong>
                    <p style="color: #15803d; margin-top: 8px; margin-bottom: 0;">
                    Follow the animation below. Inhale (4s), Hold (4s), Exhale (4s), Hold (4s).
                    </p>
                </div>
                """, unsafe_allow_html=True
            )
            st.components.v1.html(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 180px; background-color: #f8fafc; border-radius: 12px;">
                    <div style="width: 120px; height: 120px; border: 6px solid #22c55e; border-radius: 16px; animation: breathe 16s infinite; display: flex; justify-content: center; align-items: center;">
                        <span style="font-family: sans-serif; font-weight: bold; color: #166534; font-size: 1.2rem;" id="breatheText">Inhale</span>
                    </div>
                </div>
                <script>
                    const text = document.getElementById('breatheText');
                    setInterval(() => {
                        let time = (Date.now() % 16000) / 1000;
                        if(time < 4) text.innerText = 'Inhale';
                        else if(time < 8) text.innerText = 'Hold';
                        else if(time < 12) text.innerText = 'Exhale';
                        else text.innerText = 'Hold';
                    }, 100);
                </script>
                <style>
                @keyframes breathe {
                    0% { transform: scale(0.8); background-color: transparent; }
                    25% { transform: scale(1.3); background-color: rgba(34, 197, 94, 0.1); }
                    50% { transform: scale(1.3); background-color: rgba(34, 197, 94, 0.1); }
                    75% { transform: scale(0.8); background-color: transparent; }
                    100% { transform: scale(0.8); }
                }
                </style>
                """,
                height=200
            )
            
        elif cbt_exercise == "Grounding (5-4-3-2-1)":
            st.markdown(
                """
                <div style="background-color: #fff7ed; padding: 20px; border-radius: 12px; border: 1px solid #fdba74; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h4 style="color: #c2410c; margin-top: 0; display: flex; align-items: center; gap: 8px;">
                        <span>🌳</span> Grounding Technique for Anxiety
                    </h4>
                    <p style="color: #9a3412;">Take a deep breath. Look around you and slowly acknowledge:</p>
                    <ul style="color: #7c2d12; line-height: 1.8; font-size: 1.1rem; padding-left: 20px;">
                        <li><strong>5</strong> things you can <span style="color: #ea580c; font-weight: bold;">see</span> 👀</li>
                        <li><strong>4</strong> things you can <span style="color: #ea580c; font-weight: bold;">touch</span> ✋</li>
                        <li><strong>3</strong> things you can <span style="color: #ea580c; font-weight: bold;">hear</span> 👂</li>
                        <li><strong>2</strong> things you can <span style="color: #ea580c; font-weight: bold;">smell</span> 👃</li>
                        <li><strong>1</strong> thing you can <span style="color: #ea580c; font-weight: bold;">taste</span> 👅</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
