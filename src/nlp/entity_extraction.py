import re
import spacy
from typing import List, Dict, Any

# Load spaCy model with clinical entity support
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.call(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Medical entity patterns
PATTERNS = {
    "DATE_PATTERNS": [
        r"\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b",  # MM/DD/YYYY or DD/MM/YYYY
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b"  # January 1, 2023
    ],
    "PROVIDER_PATTERNS": [
        r"(?:Dr\.|Doctor|MD|DO|NP|PA)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",  # Dr. Smith
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}),\s+(?:MD|DO|NP|PA)"  # Smith, MD
    ],
    "FACILITY_PATTERNS": [
        r"(?:at|in)\s+([A-Z][A-Za-z']+(?:\s+[A-Z][A-Za-z']+){0,3})\s+(?:Hospital|Medical Center|Clinic|Center|Laboratory)",
        r"([A-Z][A-Za-z']+(?:\s+[A-Z][A-Za-z']+){0,3})\s+(?:Hospital|Medical Center|Clinic|Center|Laboratory)"
    ],
    "LAB_TEST_PATTERNS": [
        r"\b(?:CBC|Complete Blood Count|Lipid Panel|A1C|Hemoglobin A1C|TSH|Thyroid|Metabolic Panel)\b"
    ]
}

def extract_entities_from_pages(pages: List[str]) -> List[Dict[str, Any]]:
    """
    Extract medical entities from document pages
    
    Args:
        pages: List of page text strings
        
    Returns:
        List of dictionaries with extracted entities for each page
    """
    extracted = []
    
    # Track entities for propagation (Scenario 6)
    current_dos = None
    current_provider = None
    current_facility = None
    
    for idx, text in enumerate(pages):
        # Process with spaCy
        doc = nlp(text)
        
        # Initialize page entities
        page_entities = {
            "page_number": idx + 1,
            "date": None,
            "provider": None,
            "facility": None,
            "lab_tests": [],
            "medical_terms": []
        }
        
        # Extract dates
        dates = []
        for pattern in PATTERNS["DATE_PATTERNS"]:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        if dates:
            page_entities["date"] = dates[0]
            page_entities["date_candidates"] = dates
        
        # Extract providers
        for pattern in PATTERNS["PROVIDER_PATTERNS"]:
            match = re.search(pattern, text)
            if match:
                page_entities["provider"] = match.group(1) if len(match.groups()) > 0 else match.group(0)
                break
        
        # Extract facilities
        for pattern in PATTERNS["FACILITY_PATTERNS"]:
            match = re.search(pattern, text)
            if match:
                page_entities["facility"] = match.group(1) if len(match.groups()) > 0 else match.group(0)
                break
        
        # Extract lab tests
        lab_tests = []
        for pattern in PATTERNS["LAB_TEST_PATTERNS"]:
            matches = re.findall(pattern, text)
            lab_tests.extend(matches)
        
        page_entities["lab_tests"] = list(set(lab_tests))
        
        # Extract medical terms from spaCy entities
        medical_terms = []
        for ent in doc.ents:
            if ent.label_ in ["CONDITION", "DISEASE", "SYMPTOM", "TREATMENT"]:
                medical_terms.append(ent.text)
        
        page_entities["medical_terms"] = medical_terms
        
        # Handle missing information (Scenario 6)
        if not page_entities["date"] and current_dos:
            page_entities["date"] = current_dos
        else:
            current_dos = page_entities["date"]
            
        if not page_entities["provider"] and current_provider:
            page_entities["provider"] = current_provider
        else:
            current_provider = page_entities["provider"]
            
        if not page_entities["facility"] and current_facility:
            page_entities["facility"] = current_facility
        else:
            current_facility = page_entities["facility"]
        
        extracted.append(page_entities)
    
    return extracted

def get_document_timeline(entities: List[Dict[str, Any]]) -> Dict[str, List[int]]:
    """
    Create a timeline of dates and associated pages
    
    Args:
        entities: List of page entity dictionaries
        
    Returns:
        Dictionary mapping dates to page numbers
    """
    timeline = {}
    
    for entity in entities:
        if entity["date"]:
            date = entity["date"]
            if date not in timeline:
                timeline[date] = []
            timeline[date].append(entity["page_number"])
    
    return timeline
