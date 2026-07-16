import logging
from typing import Tuple, Generator, Union, Optional
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
from prompts import SYSTEM_PROMPT
import requests
import json

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

ROUTER_PROMPT = """You are a medical triage router. Analyze the following medical question and route it to the appropriate specialist agent.
Options:
1. "pharmacology" - for questions about drugs, dosages, interactions, side effects.
2. "diagnostician" - for questions about symptoms, disease identification, conditions.
3. "researcher" - for questions asking about recent news, latest guidelines, or topics not typically found in older medical textbooks.
4. "general" - for all other general medical or administrative questions.

Output ONLY the category name (e.g. pharmacology).

Question: {question}"""

PHARMACOLOGY_PROMPT = """You are a Pharmacology AI Agent.
Focus on providing safe, accurate information regarding medications, interactions, and pharmacology.
Never prescribe medication. Always advise consulting a physician.

{patient_context}

Conversation History:
{history_text}

Retrieved Medical Context:
{context}

Current Question:
{question}

Answer only from medical context.
"""

DIAGNOSTICIAN_PROMPT = """You are a Diagnostic AI Agent.
Focus on analyzing symptoms and medical conditions accurately.
Do not provide a definitive diagnosis, use language like "could be indicative of" or "is associated with".

{patient_context}

Conversation History:
{history_text}

Retrieved Medical Context:
{context}

Current Question:
{question}

Answer only from medical context.
"""

RESEARCHER_PROMPT = """You are a Medical Researcher AI Agent.
Based on the live web search results below, answer the user's question accurately.
Include citations to the sources where appropriate.

{patient_context}

Conversation History:
{history_text}

Live Web Search Context:
{context}

Current Question:
{question}
"""

GENERAL_PROMPT = """You are a Medical AI Assistant.
{patient_context}

Conversation History:
{history_text}

Retrieved Medical Context:
{context}

Current Question:
{question}

Answer only from medical context.
"""

def call_llm(prompt: str, temperature: float = 0.1, max_tokens: int = 700, privacy_mode: bool = False, stream: bool = False) -> Union[str, Generator[str, None, None]]:
    if privacy_mode:
        # Call local Ollama
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3", # default local model
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
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
        # Call Groq
        try:
            logger.info(f"Calling Groq API with model {LLM_MODEL}")
            if stream:
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                def generate():
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                return generate()
            else:
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            return f"Error calling Groq API: {e}"


def perform_web_search(query: str) -> str:
    try:
        from duckduckgo_search import DDGS
        logger.info(f"Performing web search for: {query}")
        results = DDGS().text(query, max_results=3)
        context = ""
        for r in results:
            context += f"Source: {r.get('href')}\nContent: {r.get('body')}\n\n"
        return context if context else "No relevant web search results found."
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Web search failed: {str(e)}"

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, Any

class AgentState(TypedDict):
    question: str
    context: str
    history_text: str
    patient_context: str
    patient_id: Optional[int]
    privacy_mode: bool
    language: str
    stream: bool
    
    # Internal graph state
    route: str
    sentiment: str
    pharmacology_response: str
    diagnostician_response: str
    final_prompt: str
    final_generator: Any

ROUTER_PROMPT_LG = """You are a medical triage router and sentiment analyzer. 
Analyze the following medical question and route it to the appropriate specialist agent.
Also detect the patient's emotional state (Anxious, Sad, Angry, Neutral).

Route Options:
1. "pharmacology" - for questions about drugs, dosages, interactions, side effects.
2. "diagnostician" - for questions about symptoms, disease identification, conditions.
3. "researcher" - for questions asking about recent news, latest guidelines, or topics not typically found in older medical textbooks.
4. "scheduler" - for booking appointments, taking insurance info, or patient intake.
5. "care_coordinator" - for creating medication reminders or post-op follow-up routines.
6. "complex" - if the question involves BOTH significant symptoms AND medication interactions, requiring a multi-agent debate.
7. "general" - for all other general medical or administrative questions.

Emergency Detection:
If the user mentions severe chest pain, inability to breathe, heavy bleeding, or suicide, output route "emergency".

Format your output exactly like this:
ROUTE: <category_name>
SENTIMENT: <emotion>

Question: {question}"""

SYNTHESIZER_PROMPT = """You are the Chief Medical Officer.
Review the following assessments from the Pharmacology Agent and the Diagnostic Agent.
Synthesize them into a single, cohesive, safe, and highly accurate final answer for the patient.

{patient_context}

Diagnostic Assessment:
{diagnostician_response}

Pharmacological Assessment:
{pharmacology_response}

Current Question:
{question}
"""

SCHEDULER_PROMPT = """You are a Medical Scheduling & Intake Agent.
The user wants to book an appointment or provide intake details.
Acknowledge their request, confirm the time/reason, and state that the appointment has been logged in the system.

{patient_context}

Conversation History:
{history_text}

Current Question:
{question}
"""

CARE_COORDINATOR_PROMPT = """You are a Care Coordinator AI.
The user needs a medication reminder, follow-up, or care routine set up.
Acknowledge the request, outline the care plan, and confirm that the routine has been added to their active care plan.

{patient_context}

Conversation History:
{history_text}

Current Question:
{question}
"""

def router_node(state: AgentState):
    logger.info("Executing Router Node")
    route_prompt = ROUTER_PROMPT_LG.format(question=state["question"])
    route_result = call_llm(route_prompt, temperature=0, max_tokens=30, privacy_mode=state["privacy_mode"], stream=False)
    
    route = "general"
    sentiment = "neutral"
    
    for line in str(route_result).split('\n'):
        if line.upper().startswith("ROUTE:"):
            route = line.split(":", 1)[1].strip().lower()
        elif line.upper().startswith("SENTIMENT:"):
            sentiment = line.split(":", 1)[1].strip().lower()
            
    # Hardcoded emergency keywords bypass LLM just in case
    emergency_keywords = ["suicide", "kill myself", "chest pain", "heart attack", "can't breathe", "heavy bleeding"]
    if any(k in state["question"].lower() for k in emergency_keywords):
        route = "emergency"
        sentiment = "anxious"
    
    valid_routes = ["pharmacology", "diagnostician", "researcher", "scheduler", "care_coordinator", "complex", "general", "emergency"]
    if not any(r in route for r in valid_routes):
        route = "general"
    else:
        for r in valid_routes:
            if r in route:
                route = r
                break
                
    return {"route": route, "sentiment": sentiment}

def researcher_node(state: AgentState):
    logger.info("Executing Researcher Node")
    # Override vector DB context with live web search
    new_context = perform_web_search(state["question"])
    
    prompt = RESEARCHER_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        context=new_context,
        question=state["question"]
    )
    return {"context": new_context, "final_prompt": prompt}

def diagnostician_node(state: AgentState):
    logger.info("Executing Diagnostician Node")
    prompt = DIAGNOSTICIAN_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        context=state["context"],
        question=state["question"]
    )
    if state["route"] == "complex":
        # Generate full answer non-streaming for the debate
        ans = call_llm(prompt, temperature=0.1, max_tokens=500, privacy_mode=state["privacy_mode"], stream=False)
        return {"diagnostician_response": str(ans)}
    else:
        return {"final_prompt": prompt}

def pharmacology_node(state: AgentState):
    logger.info("Executing Pharmacology Node")
    prompt = PHARMACOLOGY_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        context=state["context"],
        question=state["question"]
    )
    if state["route"] == "complex":
        # Generate full answer non-streaming for the debate
        ans = call_llm(prompt, temperature=0.1, max_tokens=500, privacy_mode=state["privacy_mode"], stream=False)
        return {"pharmacology_response": str(ans)}
    else:
        return {"final_prompt": prompt}

def general_node(state: AgentState):
    logger.info("Executing General Node")
    prompt = GENERAL_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        context=state["context"],
        question=state["question"]
    )
    return {"final_prompt": prompt}

def scheduler_node(state: AgentState):
    logger.info("Executing Scheduler Node")
    # Simulate DB insertion for MVP
    if state["patient_id"]:
        try:
            from ui.operations import add_appointment
            import datetime
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d 09:00:00")
            add_appointment(state["patient_id"], tomorrow, state["question"][:50], "Unknown Insurance")
        except Exception as e:
            logger.error(f"Failed to auto-book: {e}")
            
    prompt = SCHEDULER_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        question=state["question"]
    )
    return {"final_prompt": prompt}

def care_coordinator_node(state: AgentState):
    logger.info("Executing Care Coordinator Node")
    # Simulate DB insertion for MVP
    if state["patient_id"]:
        try:
            from ui.routines import add_care_routine
            import datetime
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            add_care_routine(state["patient_id"], "AI Assigned Routine", state["question"][:50], tomorrow)
        except Exception as e:
            logger.error(f"Failed to auto-assign routine: {e}")
            
    prompt = CARE_COORDINATOR_PROMPT.format(
        patient_context=state["patient_context"],
        history_text=state["history_text"],
        question=state["question"]
    )
    return {"final_prompt": prompt}

def synthesizer_node(state: AgentState):
    logger.info("Executing Synthesizer Node")
    prompt = SYNTHESIZER_PROMPT.format(
        patient_context=state["patient_context"],
        diagnostician_response=state.get("diagnostician_response", "No diagnostic assessment provided."),
        pharmacology_response=state.get("pharmacology_response", "No pharmacological assessment provided."),
        question=state["question"]
    )
    return {"final_prompt": prompt}

def emergency_node(state: AgentState):
    logger.info("Executing Emergency Node")
    msg = "🚨 **EMERGENCY DETECTED** 🚨\n\nYour message indicates a potential medical emergency. I am an AI and cannot provide emergency medical care.\n\n**Please call 911 or visit your nearest emergency room immediately.**\n\n*Chat paused. Handing off to human triage nurse...*"
    return {"final_generator": msg}

def generation_node(state: AgentState):
    logger.info("Executing Final Generation Node")
    final_prompt = state["final_prompt"]
    
    if state.get("sentiment") in ["anxious", "sad"]:
        final_prompt += "\n\nCRITICAL INSTRUCTION: The patient's sentiment is detected as high anxiety or sadness. You MUST respond with an extremely empathetic, calming, and supportive bedside manner."
        
    if state["language"].lower() != "english":
        final_prompt += f"\\n\\nCRITICAL INSTRUCTION: You must strictly translate and provide your final response entirely in {state['language']}. Keep the same formatting."
        
    answer = call_llm(final_prompt, temperature=0.1, max_tokens=800, privacy_mode=state["privacy_mode"], stream=state["stream"])
    return {"final_generator": answer}


def route_logic(state: AgentState):
    route = state["route"]
    if route == "emergency":
        return "emergency"
    elif route == "pharmacology":
        return "pharmacology"
    elif route == "diagnostician":
        return "diagnostician"
    elif route == "researcher":
        return "researcher"
    elif route == "scheduler":
        return "scheduler"
    elif route == "care_coordinator":
        return "care_coordinator"
    elif route == "complex":
        return ["pharmacology", "diagnostician"] # Parallel execution!
    else:
        return "general"

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("pharmacology", pharmacology_node)
builder.add_node("diagnostician", diagnostician_node)
builder.add_node("researcher", researcher_node)
builder.add_node("scheduler", scheduler_node)
builder.add_node("care_coordinator", care_coordinator_node)
builder.add_node("general", general_node)
builder.add_node("synthesizer", synthesizer_node)
builder.add_node("generator", generation_node)
builder.add_node("emergency", emergency_node)

builder.add_edge(START, "router")

# Fan-out routing: route_logic can return a string or a list of strings
builder.add_conditional_edges(
    "router",
    route_logic,
    ["pharmacology", "diagnostician", "researcher", "scheduler", "care_coordinator", "general", "emergency"]
)

# Edges from specific agents
builder.add_edge("researcher", "generator")
builder.add_edge("scheduler", "generator")
builder.add_edge("care_coordinator", "generator")
builder.add_edge("general", "generator")

# For pharma and diag, if they were part of complex, they go to synthesizer. Else generator.
def after_specialist(state: AgentState):
    if state["route"] == "complex":
        return "synthesizer"
    return "generator"

builder.add_conditional_edges("pharmacology", after_specialist, {"synthesizer": "synthesizer", "generator": "generator"})
builder.add_conditional_edges("diagnostician", after_specialist, {"synthesizer": "synthesizer", "generator": "generator"})

builder.add_edge("synthesizer", "generator")
builder.add_edge("generator", END)
builder.add_edge("emergency", END)

medical_graph = builder.compile()


def generate_agentic_response(question: str, context: str, history_text: str, patient_context: str = "", patient_id: Optional[int] = None, privacy_mode: bool = False, language: str = "English", stream: bool = False) -> Tuple[Union[str, Generator[str, None, None]], str]:
    initial_state = AgentState(
        question=question,
        context=context,
        history_text=history_text,
        patient_context=patient_context,
        patient_id=patient_id,
        privacy_mode=privacy_mode,
        language=language,
        stream=stream,
        route="general",
        pharmacology_response="",
        diagnostician_response="",
        final_prompt="",
        final_generator=None
    )
    
    # Run graph synchronously
    result_state = medical_graph.invoke(initial_state)
    
    return result_state["final_generator"], result_state["route"], result_state.get("sentiment", "neutral")

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
    # clean markdown json block if exists
    if json_str.startswith("```json"):
        json_str = json_str[7:-3]
    elif json_str.startswith("```"):
        json_str = json_str[3:-3]
    return json_str.strip()
