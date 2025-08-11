import streamlit as st

from helpers import read_csv_to_list
from model.states import NarrativeRecord
from workflow.phi_masking import phi_masking_workflow


def phi_masking_agent_app():
    """

    The PHI Masking app is a demo of a locally running LLM which can classify PHI elements in a clinical note and return
    the note with masked PHI values.
    """
    fns = [
        display_data,
        mask_sample_data,
        mask_user_data
    ]
    i = st.radio(
        "Select the function in `phi_masking_agent.py` to run:",
        options=range(len(fns)),
        format_func=lambda i: f"{fns[i].__name__}() -- {(fns[i].__doc__ or '').strip()}",
    )
    fn = fns[i]

    fn()

@st.cache_data
def get_phi_data():
    """

    Get clinical note data.

    """
    data = read_csv_to_list("sample_data.csv")
    return data

def display_data():
    """

    Display clinical note data.

    """
    data = get_phi_data()
    for row in data:
        st.write(row)

def mask_data(data):
    """

    mask data using LangGraph and on prem LLM
    """

    col1, col2 = st.columns([1,1])

    for row in data:
        with col1:
            st.write(row['narrative'])
        with col2:
            narrative= NarrativeRecord(record_id=row['id'],
                                       patient_id=row['patient_id'],
                                       narrative=row['narrative'],
                                       phi_elements=None,
                                       narrative_masked=None)
            graph = phi_masking_workflow()
            output = graph.invoke(narrative)
            st.write(output['narrative_masked'])

def mask_sample_data():
    """

    Mask PHI elements found in sample data.

    """
    sample_data = get_phi_data()
    mask_data(sample_data)

def mask_user_data():
    """

    Mask PHI elements found in user's input data.
    """
    input = st.text_input("Clinical Note", "Your note to mask...")
    user_data = [{"id":"1", "patient_id":1, "narrative":input}]
    mask_data(user_data)

if __name__ == "__main__":
    phi_masking_agent_app()