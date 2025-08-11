import json
import os
import csv
import re

from model.states import PhiElements


def read_csv_to_list(file_name):
    """
    Reads a CSV file and returns a list of dictionaries.

    Args:
        file_name (str): name of the CSV file.

    Returns:
        list: A list of dictionaries representing rows in the CSV.
    """
    # Get the directory where this script is located
    base_dir = os.path.dirname(__file__)

    # Build the path relative to this script
    file_path = os.path.join(base_dir, "data", file_name)

    data = []
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data

def parse_phi_elements_json(response_text: str) -> PhiElements:
    """
    removes /think portion of llm response
    Args:
        response_text: llm response
    Return:
        json formatted response containing location data
    """
    # Remove the <think>...</think> block
    cleaned = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)

    # Extract the JSON array (square brackets) from cleaned text
    match = re.search(r"\[.*?\]", cleaned, re.DOTALL)

    if not match:
        return []  # no JSON array found

    json_str = match.group(0)

    try:
        entities = json.loads(json_str)
    except json.JSONDecodeError:
        # Handle bad JSON if necessary
        return []

    return PhiElements(entities)