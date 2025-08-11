from langchain_core.runnables import Runnable
from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, END

from helpers import  parse_phi_elements_json
from model.states import NarrativeRecord
from prompts.phi_masking_prompt import phi_masking_prompt

# model settings
"""
llm inference runs locally with ollama. Modify model parameters here.

model should be pulled in ollama using:
ollama pull model_name
"""
llm = OllamaLLM(model="qwen3:4b",
                temperature=0.0,
                top_p=0.8,
                top_k=20)

def extract_phi_elements(state):
    """
    create llm request that applies prompt to identify locations from current event description.
    """
    chain = phi_masking_prompt | llm
    output = chain.invoke(state)
    phi_elements = parse_phi_elements_json(output)
    return {"record_id":state['record_id'],
                      "patient_id":state['patient_id'],
                      "narrative":state['narrative'],
                      "phi_elements":phi_elements,
                      "narrative_masked":None}

def replace_phi_elements(state):

    narrative = state['narrative']
    phi_elements = state['phi_elements'].data
    for element in phi_elements:
        narrative = (narrative.replace(element['value'], element['type']))
    return {"record_id":state['record_id'],
                           "patient_id":state['patient_id'],
                           "narrative":state['narrative'],
                           "phi_elements":state['phi_elements'],
                           "narrative_masked":narrative}

def phi_masking_workflow() -> Runnable:
    """
    builds simple langgraph graph
    """
    graph_builder = StateGraph(NarrativeRecord)

    graph_builder.add_node("identify_phi", extract_phi_elements)
    graph_builder.add_node("replace_phi", replace_phi_elements)

    graph_builder.set_entry_point("identify_phi")
    graph_builder.add_edge("identify_phi", "replace_phi")
    graph_builder.add_edge("replace_phi", END)

    app = graph_builder.compile()

    return app