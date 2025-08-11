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
        mask_data
    ]
    i = st.radio(
        "Select the function in `weather.py` to run:",
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

def mask_data():
    """

    Mask PHI elements found in data.

    """
    data = get_phi_data()
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


if __name__ == "__main__":
    phi_masking_agent_app()