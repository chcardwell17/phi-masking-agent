from dataclasses import dataclass
from typing import Optional, TypedDict


@dataclass
class PhiElement:
    value: str
    type: str

@dataclass
class PhiElements:
    data: list[PhiElement]


@dataclass
class NarrativeRecord(TypedDict):
    record_id: str
    patient_id: str
    narrative: str
    phi_elements: Optional[PhiElements]
    narrative_masked: Optional[str]
