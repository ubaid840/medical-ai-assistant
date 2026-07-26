import streamlit as st
from datetime import datetime
from agents import call_llm

def render_cbt_tab():
    """
    Digital CBT (Cognitive Behavioral Therapy) & Mood Journal UI
    """
    st.markdown(
        """
        <div style="
        background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(168, 85, 247, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">🧠</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Mental Wellness & Digital CBT</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Your judgment-free zone for cognitive behavioral exercises and mood tracking.</p>
        </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #c084fc, #9333ea); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(147,51,234,0.3);">
                    📊
                </div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Mood Journal</h3>
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
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #f472b6, #db2777); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(219,39,119,0.3);">
                    🧘
                </div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Digital CBT Exercises</h3>
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
