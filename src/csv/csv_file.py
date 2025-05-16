import csv
import io
import pandas as pd
from typing import List, Dict, Any, Optional, Union


def entities_to_csv(entities: List[Dict[str, Any]]) -> str:
    """
    Convert extracted entities to CSV format
    
    Args:
        entities: List of entity dictionaries extracted from document
        
    Returns:
        CSV content as string
    """
    # Create StringIO object to store CSV data
    output = io.StringIO()
    
    # Define CSV headers based on entity structure
    fieldnames = [
        'page_number', 'date', 'provider', 'facility', 
        'lab_tests', 'medical_terms'
    ]
    
    # Create CSV writer
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    
    # Process each entity for CSV export
    for entity in entities:
        row = {
            'page_number': entity.get('page_number', ''),
            'date': entity.get('date', ''),
            'provider': entity.get('provider', ''),
            'facility': entity.get('facility', ''),
            'lab_tests': '; '.join(entity.get('lab_tests', [])),
            'medical_terms': '; '.join(entity.get('medical_terms', []))
        }
        writer.writerow(row)
    
    # Return CSV content as string
    return output.getvalue()


def generate_detailed_csv(entities: List[Dict[str, Any]]) -> str:
    """
    Generate a detailed CSV with multiple sections for different entity types
    
    Args:
        entities: List of entity dictionaries extracted from document
        
    Returns:
        CSV content as string
    """
    # Create pandas DataFrame for entity summary
    df = pd.DataFrame([{
        "Page": e["page_number"],
        "Date": e.get("date", ""),
        "Provider": e.get("provider", ""),
        "Facility": e.get("facility", ""),
        "Lab Tests": "; ".join(e.get("lab_tests", [])),
        "Medical Terms": "; ".join(e.get("medical_terms", []))
    } for e in entities])
    
    # Create StringIO object for final CSV
    output = io.StringIO()
    
    # Write main entity table
    df.to_csv(output, index=False)
    output.write("\n\n")
    
    # Add provider summary section
    providers = {}
    for e in entities:
        if e.get("provider"):
            provider = e["provider"]
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(e["page_number"])
    
    if providers:
        output.write("PROVIDER SUMMARY\n")
        provider_df = pd.DataFrame([
            {"Provider": provider, "Page Count": len(pages), "Pages": ", ".join(map(str, pages))}
            for provider, pages in providers.items()
        ])
        provider_df.to_csv(output, index=False)
        output.write("\n\n")
    
    # Add facility summary section
    facilities = {}
    for e in entities:
        if e.get("facility"):
            facility = e["facility"]
            if facility not in facilities:
                facilities[facility] = []
            facilities[facility].append(e["page_number"])
    
    if facilities:
        output.write("FACILITY SUMMARY\n")
        facility_df = pd.DataFrame([
            {"Facility": facility, "Page Count": len(pages), "Pages": ", ".join(map(str, pages))}
            for facility, pages in facilities.items()
        ])
        facility_df.to_csv(output, index=False)
        output.write("\n\n")
    
    # Add date summary section
    dates = {}
    for e in entities:
        if e.get("date"):
            date = e["date"]
            if date not in dates:
                dates[date] = []
            dates[date].append(e["page_number"])
    
    if dates:
        output.write("DATE SUMMARY\n")
        date_df = pd.DataFrame([
            {"Date": date, "Page Count": len(pages), "Pages": ", ".join(map(str, pages))}
            for date, pages in dates.items()
        ])
        date_df.to_csv(output, index=False)
    
    return output.getvalue()


def generate_filtered_csv(entities: List[Dict[str, Any]], 
                          filters: Dict[str, str]) -> str:
    """
    Generate a CSV file with filtered entities based on provided criteria
    
    Args:
        entities: List of entity dictionaries extracted from document
        filters: Dictionary of filter criteria (field: value)
        
    Returns:
        CSV content as string
    """
    # Filter entities based on criteria
    filtered_entities = entities.copy()
    
    for field, value in filters.items():
        if value and value != "All":
            filtered_entities = [
                e for e in filtered_entities 
                if str(e.get(field, "")).lower() == value.lower()
            ]
    
    # Generate CSV from filtered entities
    return entities_to_csv(filtered_entities)


def generate_timeline_csv(entities: List[Dict[str, Any]]) -> str:
    """
    Generate a CSV file with timeline information
    
    Args:
        entities: List of entity dictionaries extracted from document
        
    Returns:
        CSV content as string
    """
    # Create timeline data structure
    timeline_data = {}
    
    for entity in entities:
        if entity.get("date"):
            date = entity["date"]
            if date not in timeline_data:
                timeline_data[date] = {
                    "pages": [],
                    "providers": set(),
                    "facilities": set()
                }
            
            timeline_data[date]["pages"].append(entity["page_number"])
            
            if entity.get("provider"):
                timeline_data[date]["providers"].add(entity["provider"])
                
            if entity.get("facility"):
                timeline_data[date]["facilities"].add(entity["facility"])
    
    # Convert to CSV format
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(["Date", "Pages", "Page Count", "Providers", "Facilities"])
    
    # Write data rows
    for date, data in timeline_data.items():
        writer.writerow([
            date,
            ", ".join(map(str, data["pages"])),
            len(data["pages"]),
            ", ".join(data["providers"]) if data["providers"] else "Unknown",
            ", ".join(data["facilities"]) if data["facilities"] else "Unknown"
        ])
    
    return output.getvalue()


def generate_lab_tests_csv(entities: List[Dict[str, Any]]) -> str:
    """
    Generate a CSV file focusing on lab tests
    
    Args:
        entities: List of entity dictionaries extracted from document
        
    Returns:
        CSV content as string
    """
    # Extract lab test information
    lab_data = []
    
    for entity in entities:
        page_num = entity["page_number"]
        date = entity.get("date", "Unknown")
        provider = entity.get("provider", "Unknown")
        
        for lab_test in entity.get("lab_tests", []):
            lab_data.append({
                "Page": page_num,
                "Date": date,
                "Provider": provider,
                "Lab Test": lab_test
            })
    
    # Convert to CSV
    if lab_data:
        df = pd.DataFrame(lab_data)
        return df.to_csv(index=False)
    else:
        return "No lab test data found in document"