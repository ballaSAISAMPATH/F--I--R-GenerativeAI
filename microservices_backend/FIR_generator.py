from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
from datetime import datetime
import uuid
import os
import json
import re

from encryption_template import encryption_prompt
from FIR_generation_template import FIR_generation_prompt

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


class LawSection(BaseModel):
    act_name: Optional[str] = None
    sections: List[str] = Field(default_factory=list)


class NarrationEncrypted(BaseModel):
    encrypted_narration: str
    mapping: Dict[str, Any]


class Accused(BaseModel):
    name: Optional[str] = None
    known_status: str = "unknown"
    address: Optional[str] = None
    description: Optional[str] = None


class PropertyItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[Union[str,int]] = None
    value: Optional[str] = None
    identification_marks: Optional[str] = None


class LLMFIRExtraction(BaseModel):
    acts_and_sections: List[LawSection]
    accused_list: List[Accused]
    complainant_name: Optional[str]
    complainant_address: Optional[str]
    fir_contents: str= Field(description="clear and meaningful summary of the story and the fir")
    property_details: List[PropertyItem]
    total_property_value: Optional[str]
    delay_in_reporting_reason: Optional[str]
    action_taken_description: Optional[str]
    date_of_occurrence: Optional[str]
    time_of_occurrence: Optional[str]
    place_of_occurrence: Optional[str]

class FIRFormIF1(BaseModel):
    district: Optional[str]
    police_station: Optional[str]
    year: Optional[str]
    fir_number: Optional[str]
    fir_date: Optional[str]
    date_of_occurrence: Optional[str]
    time_of_occurrence: Optional[str]
    acts_and_sections: List[LawSection] = Field(default_factory=list)
    other_acts_and_sections: Optional[str] = None
    place_of_occurrence: Optional[str]
    information_received_date: Optional[str]
    information_received_time: Optional[str]
    general_diary_entry_numbers: Optional[str]
    general_diary_time: Optional[str]

    distance_and_direction_from_ps: Optional[str]

    complainant_name: Optional[str]
    complainant_address: Optional[str]

    accused_list: List[Accused] = Field(default_factory=list)

    property_details: List[PropertyItem] = Field(default_factory=list)
    total_property_value: Optional[str]

    delay_in_reporting_reason: Optional[str]

    fir_contents: Optional[str]

    action_taken_description: Optional[str]



def get_current_datetime():
    now = datetime.now()
    return {
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%H:%M:%S"),
        "year": now.strftime("%Y")
    }


def generate_fir_number():
    return f"FIR-{uuid.uuid4().hex[:8].upper()}"


def get_device_location():
    return {
        "district": "Visakhapatnam",
        "police_station": "Cyber Crime Police Station",
        "distance_and_direction_from_ps": "2 KM North"
    }


model1 = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
    format="json"


)
llm_extraction = model.with_structured_output(LLMFIRExtraction)

def encrypt_narration(state: dict):
    msg = encryption_prompt.format_messages(
        text=state["fir_text"]
    ) 
    response = model1.invoke(msg)

    data = json.loads(response.content)

    # Normalize mapping keys (strip whitespace, uppercase) to ensure consistent matching
    raw_mapping = data.get("mapping", {})
    normalized_mapping = {k.strip().upper(): v for k, v in raw_mapping.items()}

    # Also normalize placeholders in the encrypted narration to match
    encrypted = data["encrypted_narration"]
    for original_key, normalized_key in zip(raw_mapping.keys(), normalized_mapping.keys()):
        encrypted = encrypted.replace(original_key, normalized_key)

    print("\n[encrypt_narration] mapping keys:", list(normalized_mapping.keys()))
    print("[encrypt_narration] encrypted narration snippet:", encrypted[:200])

    return {
        "encrypted_narration": encrypted,
        "mapping": normalized_mapping
    }


def llm_extract_fields(state: dict):
    msg = FIR_generation_prompt.format_messages(
        FIR_narration=state["encrypted_narration"]
    )
    extracted = llm_extraction.invoke(msg)
    return {
        "llm_data": extracted,
        "mapping": state["mapping"]
    }

def replace_secured_fields(value, mapping: dict):
    if isinstance(value, str):
        for placeholder, original in mapping.items():
            value = value.replace(placeholder, str(original))
        return value

    if isinstance(value, list):
        return [replace_secured_fields(v, mapping) for v in value]

    if isinstance(value, dict):
        return {k: replace_secured_fields(v, mapping) for k, v in value.items()}

    return value


def mapping_function(state: dict):
    llm_data = state["llm_data"]
    raw_mapping = state["mapping"]

    # Normalize: strip whitespace from keys so Ollama inconsistencies don't break matching
    mapping = {k.strip(): v for k, v in raw_mapping.items()}

    print("\n[mapping_function] mapping keys:", list(mapping.keys()))

    secured_data = llm_data.model_dump()
    restored_data = replace_secured_fields(secured_data, mapping)

    # Warn about any leftover placeholders (pattern: WORD_NUMBER)
    placeholder_pattern = re.compile(r'\b[A-Z]+_\d+\b')
    for field, val in restored_data.items():
        if isinstance(val, str):
            leftovers = placeholder_pattern.findall(val)
            if leftovers:
                print(f"[mapping_function] WARNING: unresolved placeholders in '{field}': {leftovers}")

    restored_llm_data = LLMFIRExtraction(**restored_data)

    return {
        "llm_data": restored_llm_data
    }


def build_final_fir(state: dict):
    dt = get_current_datetime()
    loc = get_device_location()
    llm = state["llm_data"]
    

    fir = FIRFormIF1(
        district=loc["district"],
        police_station=loc["police_station"],
        year=dt["year"],
        fir_number=generate_fir_number(),
        date_of_occurrence=llm.date_of_occurrence,
        time_of_occurrence=llm.time_of_occurrence,
        fir_date=dt["date"],
        information_received_date=dt["date"],
        information_received_time=dt["time"],
        general_diary_entry_numbers="AUTO",
        general_diary_time=dt["time"],
        distance_and_direction_from_ps=loc["distance_and_direction_from_ps"],
        place_of_occurrence=llm.place_of_occurrence,
        acts_and_sections=llm.acts_and_sections,
        accused_list=llm.accused_list,
        complainant_name=llm.complainant_name,
        complainant_address=llm.complainant_address,
        fir_contents=llm.fir_contents,
        property_details=llm.property_details,
        total_property_value=llm.total_property_value,
        delay_in_reporting_reason=llm.delay_in_reporting_reason,

        action_taken_description=llm.action_taken_description
    )

    return {"fir": fir}

def validate_extraction(state: dict):
    llm = state["llm_data"]

    missing_fields = []

    if not llm.complainant_name:
        missing_fields.append("complainant_name")
    if not llm.place_of_occurrence:
        missing_fields.append("place_of_occurrence")
    if not llm.date_of_occurrence:
        missing_fields.append("date_of_occurrence")

    return {
        **state,   
        "missing_fields": missing_fields,
        "retry_count": state.get("retry_count", 0)
    }
   

def decide_next_step(state: dict):
    if state["missing_fields"] and state["retry_count"] < 2:
        return "retry_extraction"
    return "mapping_function"

def retry_extraction(state: dict):
    msg = FIR_generation_prompt.format_messages(
        FIR_narration=state["encrypted_narration"]
    )

    extracted = llm_extraction.invoke(msg)

    return {
        **state,   
        "llm_data": extracted,
        "retry_count": state["retry_count"] + 1
    }

graph = StateGraph(dict)

graph.add_node("encrypt_narration", encrypt_narration)
graph.add_node("llm_extract_fields", llm_extract_fields)
graph.add_node("validate_extraction", validate_extraction)
graph.add_node("retry_extraction", retry_extraction)
graph.add_node("mapping_function", mapping_function)
graph.add_node("build_final_fir", build_final_fir)

graph.add_edge(START, "encrypt_narration")
graph.add_edge("encrypt_narration", "llm_extract_fields")

# NEW FLOW
graph.add_edge("llm_extract_fields", "validate_extraction")

graph.add_conditional_edges(
    "validate_extraction",
    decide_next_step,
    {
        "retry_extraction": "retry_extraction",
        "mapping_function": "mapping_function"
    }
)

graph.add_edge("retry_extraction", "validate_extraction")

graph.add_edge("mapping_function", "build_final_fir")
graph.add_edge("build_final_fir", END)

compiled_graph = graph.compile()


# FIR_TEXT = """
# On 15th April 2025, the complainant Rahul Mehta, aged 32 years,
# resident of Secunderabad, received multiple phone calls and WhatsApp
# messages from an unknown person claiming to be a bank officer.
# The accused obtained debit card details and OTP and transferred
# ₹1,20,000/- online. The accused threatened false cases if reported.
# """

# output = compiled_graph.invoke({"fir_text": FIR_TEXT})

# print(json.dumps(output["fir"].model_dump(), indent=2))