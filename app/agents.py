from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
from prompts import SYSTEM_PROMPT
import requests
import json

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

def call_llm(prompt, temperature=0.1, max_tokens=700, privacy_mode=False):
    if privacy_mode:
        # Call local Ollama
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3", # default local model
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Error connecting to local Ollama in Privacy Mode: {e}"
    else:
        # Call Groq
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()


def perform_web_search(query):
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=3)
        context = ""
        for r in results:
            context += f"Source: {r.get('href')}\nContent: {r.get('body')}\n\n"
        return context if context else "No relevant web search results found."
    except Exception as e:
        return f"Web search failed: {str(e)}"

def generate_agentic_response(question, context, history_text, patient_context="", privacy_mode=False, language="English"):
    # 1. Route
    route_prompt = ROUTER_PROMPT.format(question=question)
    route = call_llm(route_prompt, temperature=0, max_tokens=10, privacy_mode=privacy_mode).lower()
    
    # 2. Setup prompts and fallback context
    if "pharmacology" in route:
        prompt = PHARMACOLOGY_PROMPT
    elif "diagnostician" in route:
        prompt = DIAGNOSTICIAN_PROMPT
    elif "researcher" in route:
        prompt = RESEARCHER_PROMPT
        # Override vector DB context with live web search
        context = perform_web_search(question)
    else:
        prompt = GENERAL_PROMPT
        route = "general" # fallback clean

    final_prompt = prompt.format(
        patient_context=patient_context,
        history_text=history_text,
        context=context,
        question=question
    )

    if language.lower() != "english":
        final_prompt += f"\n\nCRITICAL INSTRUCTION: You must strictly translate and provide your final response entirely in {language}. Keep the same formatting."

    answer = call_llm(final_prompt, temperature=0.1, max_tokens=700, privacy_mode=privacy_mode)
    return answer, route

def generate_soap_note(history_text, patient_context="", privacy_mode=False):
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
    return call_llm(soap_prompt, temperature=0, max_tokens=800, privacy_mode=privacy_mode)

def generate_fhir_json(soap_text, patient_context="", privacy_mode=False):
    fhir_prompt = f"""You are a healthcare data engineer. Convert the following SOAP note and patient context into a simplified FHIR JSON structure (e.g. Patient resource, Condition, Observation, CarePlan).

{patient_context}
{soap_text}

Output ONLY valid JSON.
"""
    json_str = call_llm(fhir_prompt, temperature=0, max_tokens=1200, privacy_mode=privacy_mode)
    # clean markdown json block if exists
    if json_str.startswith("```json"):
        json_str = json_str[7:-3]
    elif json_str.startswith("```"):
        json_str = json_str[3:-3]
    return json_str.strip()
