import logging
from typing import Tuple, Generator, Union, Optional, List, Dict
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
import requests
import json
from privacy_manager import PrivacyManager

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

# ==============================================================================
# PROMPTS
# ==============================================================================

EXPLAINABILITY_FOOTER = """
---
**AI Reasoning & Explainability**
- **Confidence:** [High/Medium/Low]
- **Supporting Evidence:** [Key facts used]
- **Contradictory/Missing Info:** [Any missing data or conflicting symptoms]
- **Recommended Next Steps:** [Actionable clinical steps]
"""

ROUTER_PROMPT_LG = """You are the Chief Medical AI Router for a 20-Agent Swarm. 
Analyze the following medical question and route it to the appropriate specialist agents.
CRITICAL API SAFEGUARD: You MUST select EXACTLY 2 or 3 of the most relevant agents. NEVER select more than 3.
Also detect the patient's emotional state (Anxious, Sad, Angry, Neutral).

Route Options (select 2 or 3 separated by comma):
- "physician_ai" (internal medicine)
- "surgeon_ai" (surgery, trauma)
- "radiology_ai" (imaging)
- "pathology_ai" (labs, tissue)
- "genomics_ai" (DNA, genetics)
- "pharmacy_ai" (medications, pharmacology)
- "nutrition_ai" (diet, metabolism)
- "mental_health_ai" (psychiatry)
- "insurance_ai" (billing, coding)
- "research_ai" (clinical trials)
- "ethics_ai" (medical ethics)
- "qa_ai" (quality assurance)
- "cardiology_ai" (heart, blood pressure)
- "oncology_ai" (cancer, tumors)
- "neurology_ai" (brain, nerves)
- "infectious_disease_ai" (viruses, bacteria, sepsis)
- "endocrinology_ai" (hormones, diabetes)
- "pediatrics_ai" (children, infants)
- "rehabilitation_ai" (physical therapy, recovery)
- "safety_verification_ai" (verifies high-risk claims)
- "emergency_triage" (ONLY use if life-threatening)

Format your output exactly like this:
ROUTE: <agent_1, agent_2, agent_3>
SENTIMENT: <emotion>

Question: {question}"""

DIAGNOSTICIAN_PROMPT = """You are an AI Clinical Reasoning Engine & Diagnostician.
Perform advanced clinical reasoning simulating a clinician's thought process.

Based on the symptoms, provide a **Differential Diagnosis Ranking** with Bayesian probability estimates.
Check for contradictions and identify missing information.

Format Example:
Possible Diagnoses
------------------
Disease A          63%
Disease B          16%

Reason:
✓ Symptom 1 matches
✓ Risk factor X matches

CRITICAL ANTI-HALLUCINATION RULE: If a term is unrecognized, check if it is a likely typo for a known medical term. If it is a typo, state the assumption and proceed with the correct term. If completely unrecognized, politely state that you do not recognize it. Use ONLY provided context or general, well-established medical knowledge.

{patient_context}

Conversation History:
{history_text}

Retrieved Medical Context:
{context}

Current Question:
{question}
""" + EXPLAINABILITY_FOOTER

SPECIALIST_TEMPLATE = """You are a highly specialized {specialty} AI Agent.
Focus on providing safe, accurate, evidence-based information regarding {focus}.

CRITICAL ANTI-HALLUCINATION RULE: If a term is unrecognized, check if it is a likely typo for a known medical term. If it is a typo, state the assumption and proceed with the correct term. If completely unrecognized, politely state that you do not recognize it. Use ONLY provided context or general, well-established medical knowledge.

{patient_context}

Conversation History:
{history_text}

Retrieved Medical Context:
{context}

Current Question:
{question}
""" + EXPLAINABILITY_FOOTER

SYNTHESIZER_PROMPT = """You are the Chief Medical AI Coordinator.
Synthesize the independent assessments and any internal debate conclusions from your specialized medical agents into a single, cohesive, highly professional clinical response.

Patient Context: {patient_context}

Agent Assessments:
{agent_responses}

Question: {question}

IMPORTANT: You are the Clinical Uncertainty Engine (Feature 29). Do NOT provide a single definitive answer. 
CRITICAL ADVANCED RAG INSTRUCTION: You MUST explicitly ground your response in the provided Medical Context. Cite "Verified Medical Encyclopedias and Clinical Guidelines" when detailing your evidence. DO NOT hallucinate statistics or treatments not present in the medical consensus.

You MUST format your final output using exactly these sections:

### 🏆 Diagnostic Tournament Consensus
[Synthesize the debate and consensus]

### 📚 Verified RAG Sources
[Explicitly list the clinical guidelines or medical encyclopedias referenced in the context]

### 📊 Ranked Possibilities
1. [Condition A] - [Confidence: High/Medium/Low]
2. [Condition B] - [Confidence: High/Medium/Low]

### 🔬 Supporting Evidence
[List evidence supporting the ranked options based on agent input and RAG context]

### ❓ Missing Information
[List 2-3 pieces of missing data/tests that would drastically improve confidence]

### 🩺 Recommended Next Steps
[Actionable clinical steps]
"""

RESEARCHER_PROMPT = SPECIALIST_TEMPLATE.format(specialty="Medical Researcher", focus="recent medical literature, clinical trials, and guidelines", patient_context="{patient_context}", history_text="{history_text}", context="{context}", question="{question}")
GENERAL_PROMPT = SPECIALIST_TEMPLATE.format(specialty="General Medical", focus="general medical inquiries", patient_context="{patient_context}", history_text="{history_text}", context="{context}", question="{question}")
SCHEDULER_PROMPT = """You are a Medical Scheduling & Intake Agent. Acknowledge the request and confirm the time/reason has been logged.
{patient_context}
Conversation History: {history_text}
Current Question: {question}"""
CARE_COORDINATOR_PROMPT = """You are a Care Coordinator AI. Acknowledge the request, outline the care plan, and confirm it's added.
{patient_context}
Conversation History: {history_text}
Current Question: {question}"""

def call_llm(prompt: str, temperature: float = 0.1, max_tokens: int = 800, privacy_mode: bool = False, stream: bool = False, override_model: str = None) -> Union[str, Generator[str, None, None]]:
    if privacy_mode:
        url = "http://localhost:11434/api/generate"
        payload = {"model": "llama3", "prompt": prompt, "stream": stream, "options": {"temperature": temperature, "num_predict": max_tokens}}
        try:
            logger.info("Calling local Ollama API")
            if stream:
                response = requests.post(url, json=payload, stream=True)
                response.raise_for_status()
                def generate():
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            yield data.get("response", "")
                return generate()
            else:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                return response.json().get("response", "").strip()
        except Exception as e:
            logger.error(f"Error connecting to local Ollama in Privacy Mode: {e}")
            return f"Error connecting to local Ollama in Privacy Mode: {e}"
    else:
        try:
            active_model = override_model if override_model else LLM_MODEL
            logger.info(f"Calling Groq API with model {active_model}")
            if stream:
                response = client.chat.completions.create(model=active_model, messages=[{"role": "user", "content": prompt}], temperature=temperature, max_tokens=max_tokens, stream=True)
                def generate():
                    for chunk in response:
                        if chunk.choices[0].delta.content: yield chunk.choices[0].delta.content
                return generate()
            else:
                response = client.chat.completions.create(model=active_model, messages=[{"role": "user", "content": prompt}], temperature=temperature, max_tokens=max_tokens)
                return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            return f"Error calling Groq API: {e}"

def perform_web_search(query: str) -> str:
    try:
        from ddgs import DDGS
        logger.info(f"Performing web search for: {query}")
        results = DDGS().text(query, max_results=3)
        context = ""
        for r in results: context += f"Source: {r.get('href')}\nContent: {r.get('body')}\n\n"
        return context if context else "No relevant web search results found."
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Web search failed: {str(e)}"

# ==============================================================================
# LANGGRAPH STATE & NODES
# ==============================================================================

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Any, Annotated

def merge_responses(a: dict, b: dict) -> dict:
    res = (a or {}).copy()
    res.update(b or {})
    return res

class AgentState(TypedDict):
    question: str
    context: str
    history_text: str
    patient_context: str
    patient_id: Optional[int]
    privacy_mode: bool
    language: str
    stream: bool
    is_emergency: bool
    triage_score: int
    compliance_region: str
    
    route: str
    routes: List[str]
    sentiment: str
    agent_responses: Annotated[Dict[str, str], merge_responses]
    debate_summary: str  # NEW: For storing the debate output
    final_prompt: str
    final_generator: Any

def router_node(state: AgentState):
    logger.info("Executing Chief Medical AI Router Node")
    route_prompt = ROUTER_PROMPT_LG.format(question=state["question"])
    route_result = call_llm(route_prompt, temperature=0, max_tokens=50, privacy_mode=state["privacy_mode"], stream=False)
    
    routes = ["physician_ai"] # default fallback
    sentiment = "neutral"
    
    for line in str(route_result).split('\n'):
        if line.upper().startswith("ROUTE:"):
            route_str = line.split(":", 1)[1].strip().lower()
            routes = [r.strip() for r in route_str.split(",")]
        elif line.upper().startswith("SENTIMENT:"):
            sentiment = line.split(":", 1)[1].strip().lower()
            
    # Automated Clinical Triage: Dynamic Severity Scoring
    triage_score = 1 # Default
    question_lower = state["question"].lower()
    
    mild_keywords = ["headache", "cough", "rash", "tired"]
    mod_keywords = ["fever", "vomiting", "dizzy", "pain"]
    severe_keywords = ["suicide", "kill myself", "chest pain", "heart attack", "can't breathe", "heavy bleeding", "stroke", "unconscious"]
    
    if any(k in question_lower for k in mild_keywords): triage_score = max(triage_score, 3)
    if any(k in question_lower for k in mod_keywords): triage_score = max(triage_score, 6)
    if any(k in question_lower for k in severe_keywords): triage_score = 9
    
    if triage_score >= 7:
        routes = ["emergency_triage"]
        sentiment = "anxious"
    
    valid_routes = [
        "physician_ai", "surgeon_ai", "radiology_ai", "pathology_ai",
        "genomics_ai", "pharmacy_ai", "nutrition_ai", "mental_health_ai",
        "insurance_ai", "research_ai", "ethics_ai", "qa_ai", 
        "cardiology_ai", "oncology_ai", "neurology_ai", "infectious_disease_ai",
        "endocrinology_ai", "pediatrics_ai", "rehabilitation_ai", "safety_verification_ai",
        "emergency_triage"
    ]
    
    filtered_routes = [r for r in routes if r in valid_routes]
    
    # API DESTRUCTION SAFEGUARD: Enforce absolute maximum of 3 agents
    if len(filtered_routes) > 3:
        logger.warning(f"API Safeguard Triggered: Router requested {len(filtered_routes)} agents. Truncating to 3.")
        filtered_routes = filtered_routes[:3]
        
    if not filtered_routes:
        filtered_routes = ["physician_ai"]
        
    return {"route": "complex" if len(filtered_routes) > 1 else filtered_routes[0], "routes": filtered_routes, "sentiment": sentiment, "agent_responses": {}, "debate_summary": "", "triage_score": triage_score}

def calculator_node(state: AgentState):
    from medical_calculator import calculate_bmi, calculate_map, calculate_egfr
    extract_prompt = f"""Extract JSON parameters for calc: bmi, map, or egfr.
Question: {state['question']}"""
    json_result = call_llm(extract_prompt, temperature=0, max_tokens=150, privacy_mode=state["privacy_mode"], stream=False)
    try:
        json_str = str(json_result).strip()
        if json_str.startswith("```json"): json_str = json_str[7:-3]
        elif json_str.startswith("```"): json_str = json_str[3:-3]
        import json
        params = json.loads(json_str)
        if params.get("calc") == "bmi": calc_result = calculate_bmi(params.get("weight_kg", 0), params.get("height_m", 0))
        elif params.get("calc") == "map": calc_result = calculate_map(params.get("systolic", 0), params.get("diastolic", 0))
        elif params.get("calc") == "egfr": calc_result = calculate_egfr(params.get("creatinine", 1.0), params.get("age", 50), params.get("is_female", False), params.get("is_black", False))
        else: calc_result = "Unsupported calculation."
    except Exception as e:
        calc_result = f"Parse failed. {e}"
    prompt = f"Calculation Result: {calc_result}\nExplain it to the user.\nQuestion: {state['question']}\n{EXPLAINABILITY_FOOTER}"
    return {"final_prompt": prompt}

def researcher_node(state: AgentState):
    new_context = perform_web_search(state["question"])
    prompt = RESEARCHER_PROMPT.format(patient_context=state["patient_context"], history_text=state["history_text"], context=new_context, question=state["question"])
    return {"context": new_context, "final_prompt": prompt}

def _specialist_node(state: AgentState, specialty: str, focus: str, template: str = SPECIALIST_TEMPLATE):
    prompt = template.format(specialty=specialty, focus=focus, patient_context=state["patient_context"], history_text=state["history_text"], context=state["context"], question=state["question"])
    if len(state["routes"]) > 1:
        ans = call_llm(prompt, temperature=0.1, max_tokens=500, privacy_mode=state["privacy_mode"], stream=False, override_model="llama-3.3-70b-versatile")
        return {"agent_responses": {specialty.lower(): str(ans)}}
    return {"final_prompt": prompt}

def physician_ai_node(state: AgentState): return _specialist_node(state, "Physician AI", "internal medicine, diagnosis, and non-surgical treatment")
def surgeon_ai_node(state: AgentState): return _specialist_node(state, "Surgeon AI", "surgical interventions, perioperative care, and trauma")
def radiology_ai_node(state: AgentState): return _specialist_node(state, "Radiology AI", "medical imaging interpretation (X-Ray, MRI, CT)")
def pathology_ai_node(state: AgentState): return _specialist_node(state, "Pathology AI", "tissue analysis, cellular biology, and lab tests")
def genomics_ai_node(state: AgentState): return _specialist_node(state, "Genomics AI", "DNA sequencing, hereditary risk, and pharmacogenomics")
def pharmacy_ai_node(state: AgentState): return _specialist_node(state, "Pharmacy AI", "drug interactions, pharmacokinetics, and safe dosing")
def nutrition_ai_node(state: AgentState): return _specialist_node(state, "Nutrition AI", "metabolic health, dietetics, and supplementation")
def mental_health_ai_node(state: AgentState): return _specialist_node(state, "Mental Health AI", "psychiatry, mood disorders, and digital CBT")
def insurance_ai_node(state: AgentState): return _specialist_node(state, "Insurance AI", "medical coding, billing, and coverage analysis")
def research_ai_node(state: AgentState): return _specialist_node(state, "Research AI", "clinical trials, experimental treatments, and novel literature")
def ethics_ai_node(state: AgentState): return _specialist_node(state, "Ethics AI", "medical ethics, informed consent, and end-of-life care")
def qa_ai_node(state: AgentState): return _specialist_node(state, "Quality Assurance AI", "verifying clinical safety, flagging contradictions, and ensuring standard of care")
def cardiology_ai_node(state: AgentState): return _specialist_node(state, "Cardiology AI", "cardiovascular health, blood pressure, and heart disease")
def oncology_ai_node(state: AgentState): return _specialist_node(state, "Oncology AI", "cancer diagnosis, tumors, and chemotherapy")
def neurology_ai_node(state: AgentState): return _specialist_node(state, "Neurology AI", "brain function, nerve disorders, and cognitive decline")
def infectious_disease_ai_node(state: AgentState): return _specialist_node(state, "Infectious Disease AI", "viruses, bacteria, sepsis, and pandemics")
def endocrinology_ai_node(state: AgentState): return _specialist_node(state, "Endocrinology AI", "hormones, diabetes, and metabolic disorders")
def pediatrics_ai_node(state: AgentState): return _specialist_node(state, "Pediatrics AI", "childhood development, infant care, and pediatric medicine")
def rehabilitation_ai_node(state: AgentState): return _specialist_node(state, "Rehabilitation AI", "physical therapy, recovery, and kinesiology")
def safety_verification_ai_node(state: AgentState): return _specialist_node(state, "Safety Verification AI", "verifying claims against trusted medical references and flagging high-risk clinical advice")

def emergency_triage_node(state: AgentState):
    msg = "🚨 **EMERGENCY TRIAGE DETECTED** 🚨\n\nYour symptoms indicate a potential medical emergency. I am an AI and cannot provide emergency medical care.\n\n**Please call 911 or visit your nearest emergency room immediately.**"
    return {"final_generator": msg, "is_emergency": True}

def debate_node(state: AgentState):
    logger.info("Executing Autonomous Debate Node")
    responses_text = "\n\n".join([f"--- {k.upper()} ---\n{v}" for k, v in state["agent_responses"].items()])
    debate_prompt = f"""You are the Chief Medical AI moderating a debate between specialized agents.
Review the following independent assessments. 
Identify any contradictions, agreements, or oversights between the agents.
Write a concise "Debate Conclusion" resolving the conflict before final synthesis.

Agent Assessments:
{responses_text}

Debate Conclusion:"""
    debate_result = call_llm(debate_prompt, temperature=0.3, max_tokens=400, privacy_mode=state["privacy_mode"], stream=False, override_model="llama-3.3-70b-versatile")
    return {"debate_summary": str(debate_result)}

def synthesizer_node(state: AgentState):
    logger.info("Executing Chief Medical AI Synthesizer Node")
    responses_text = "\n\n".join([f"--- {k.upper()} ---\n{v}" for k, v in state["agent_responses"].items()])
    if state["debate_summary"]:
        responses_text += f"\n\n--- INTERNAL DEBATE CONCLUSION ---\n{state['debate_summary']}"
        
    prompt = SYNTHESIZER_PROMPT.format(patient_context=state["patient_context"], agent_responses=responses_text, question=state["question"])
    return {"final_prompt": prompt}

def generation_node(state: AgentState):
    logger.info("Executing Final Generation Node")
    final_prompt = state.get("final_prompt", "")
    
    sentiment = state.get("sentiment", "neutral")
    if sentiment in ["anxious", "sad"]:
        final_prompt = "CRITICAL: Patient sentiment is HIGH ANXIETY/SADNESS. Use Digital CBT techniques. Start with profound, judgment-free empathy before medical info.\n\n" + final_prompt
    elif sentiment == "angry":
        final_prompt = "CRITICAL: Patient is ANGRY. Use de-escalation. Be extremely polite and concise.\n\n" + final_prompt
        
    if state["language"].lower() != "english":
        final_prompt += f"\n\nCRITICAL: Strictly translate and provide your final response entirely in {state['language']}. Keep formatting."
        
    compliance = state.get("compliance_region", "US (FDA / HIPAA)")
    final_prompt += f"\n\nCOMPLIANCE DIRECTIVE: You MUST strictly adhere to the medical protocols, approved drug formularies, and privacy laws of this region: {compliance}. Do not recommend drugs or procedures unapproved in this region."
        
    if "diagnostician" in state["routes"] or len(state["routes"]) > 1:
        answer = call_llm(final_prompt, temperature=0.1, max_tokens=1000, privacy_mode=state["privacy_mode"], stream=state["stream"], override_model="llama-3.3-70b-versatile")
    else:
        answer = call_llm(final_prompt, temperature=0.1, max_tokens=800, privacy_mode=state["privacy_mode"], stream=state["stream"])
        
    return {"final_generator": answer}

def route_logic(state: AgentState):
    if "emergency_triage" in state["routes"]: return "emergency_triage"
    if len(state["routes"]) > 1: return state["routes"]
    return state["routes"][0] if state["routes"] else "physician_ai"

# Define all 20 specialists for routing
specialists = [
    "physician_ai", "surgeon_ai", "radiology_ai", "pathology_ai",
    "genomics_ai", "pharmacy_ai", "nutrition_ai", "mental_health_ai",
    "insurance_ai", "research_ai", "ethics_ai", "qa_ai",
    "cardiology_ai", "oncology_ai", "neurology_ai", "infectious_disease_ai",
    "endocrinology_ai", "pediatrics_ai", "rehabilitation_ai", "safety_verification_ai"
]

builder = StateGraph(AgentState)
builder.add_node("router", router_node)
for sp in specialists:
    builder.add_node(sp, globals()[f"{sp}_node"])
builder.add_node("debate", debate_node)
builder.add_node("synthesizer", synthesizer_node)
builder.add_node("generator", generation_node)
builder.add_node("emergency_triage", emergency_triage_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_logic,
    specialists + ["emergency_triage"]
)

def after_specialist(state: AgentState):
    return "debate" if len(state["routes"]) > 1 else "generator"

for sp in specialists:
    builder.add_conditional_edges(sp, after_specialist, {"debate": "debate", "generator": "generator"})

builder.add_edge("debate", "synthesizer")
builder.add_edge("synthesizer", "generator")
builder.add_edge("generator", END)
builder.add_edge("emergency_triage", END)

medical_graph = builder.compile()


def generate_agentic_response(question: str, context: str, history_text: str, patient_context: str = "", patient_id: Optional[int] = None, privacy_mode: bool = False, language: str = "English", compliance_region: str = "US (FDA / HIPAA)", stream: bool = False) -> Tuple[Union[str, Generator[str, None, None]], str, str, bool, int]:
    
    safe_question = PrivacyManager.mask_phi(question)
    safe_history = PrivacyManager.mask_phi(history_text)
    
    initial_state = AgentState(
        question=safe_question,
        context=context,
        history_text=safe_history,
        patient_context=patient_context,
        patient_id=patient_id,
        privacy_mode=privacy_mode,
        language=language,
        compliance_region=compliance_region,
        stream=stream,
        is_emergency=False,
        triage_score=1,
        route="general",
        routes=[],
        sentiment="neutral",
        agent_responses={},
        debate_summary="",
        final_prompt="",
        final_generator=None
    )
    
    result_state = medical_graph.invoke(initial_state)
    
    return result_state["final_generator"], result_state["route"], result_state.get("sentiment", "neutral"), result_state.get("is_emergency", False), result_state.get("triage_score", 1)

def generate_soap_note(history_text: str, patient_context: str = "", privacy_mode: bool = False) -> str:
    soap_prompt = f"""You are a medical scribe. Based on the following patient conversation, generate a professional clinical SOAP note.

{patient_context}

Conversation:
{history_text}

Please format as:
## SOAP Note
**S (Subjective):** ...
**O (Objective):** ...
**A (Assessment):** ...
**P (Plan):** ...
"""
    result = call_llm(soap_prompt, temperature=0, max_tokens=800, privacy_mode=privacy_mode, stream=False)
    return str(result)

def generate_fhir_json(soap_text: str, patient_context: str = "", privacy_mode: bool = False) -> str:
    fhir_prompt = f"""You are a healthcare data engineer. Convert the following SOAP note and patient context into a simplified FHIR JSON structure (e.g. Patient resource, Condition, Observation, CarePlan).

{patient_context}
{soap_text}

Output ONLY valid JSON.
"""
    json_result = call_llm(fhir_prompt, temperature=0, max_tokens=1200, privacy_mode=privacy_mode, stream=False)
    json_str = str(json_result)
    if json_str.startswith("```json"):
        json_str = json_str[7:-3]
    elif json_str.startswith("```"):
        json_str = json_str[3:-3]
    return json_str.strip()
