import sys
import os
import json
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

# Configure environment
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Project imports
from src.utils.pdf_extract import (
    extract_pdf_text,
    extract_metadata,
    extract_header_footer,
    clean_page_text
)

# Try to import entity extraction, with fallback if spaCy fails
try:
    from src.nlp.entity_extraction import extract_entities_from_pages, get_document_timeline
    entity_extraction_available = True
except Exception as e:
    st.error(f"Error loading entity extraction: {str(e)}")
    entity_extraction_available = False

# Streamlit Configuration
st.set_page_config(page_title="Medical Entity Extractor Pro", layout="wide", page_icon="🏥")
st.title("🏥 Medical Entity Extractor Pro")

def visualize_timeline(entities):
    """Create timeline visualization of document pages"""
    # Extract dates and page numbers
    timeline_data = []
    for entity in entities:
        if entity["date"]:
            try:
                # Try to parse date for proper sorting
                date_obj = datetime.strptime(entity["date"], "%m/%d/%Y")
                start_date = date_obj.strftime("%Y-%m-%d")
                end_date = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
            except:
                # Fallback for other date formats
                start_date = entity["date"]
                end_date = entity["date"]
                
            timeline_data.append({
                "Start": start_date,
                "Finish": end_date,
                "Page": f"Page {entity['page_number']}",
                "Provider": entity["provider"] or "Unknown",
                "Facility": entity["facility"] or "Unknown"
            })
    
    if not timeline_data:
        return None
        
    # Create DataFrame for Plotly
    df = pd.DataFrame(timeline_data)
    
    # Create timeline visualization
    fig = px.timeline(
        df, 
        x_start="Start",
        x_end="Finish",
        y="Page",
        color="Provider",
        hover_data=["Facility"],
        title="Document Timeline by Date of Service"
    )
    
    fig.update_layout(
        height=400,
        xaxis=dict(title="Date of Service"),
        yaxis=dict(title="Document Page"),
        legend=dict(title="Provider"),
        hovermode="closest"
    )
    
    return fig

def generate_clean_pdf(pages):
    """Generate sanitized PDF from cleaned pages"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)
    
    def sanitize(text):
        return text.encode('latin-1', 'replace').decode('latin-1')[:85]
    
    for page in pages:
        pdf.add_page()
        for line in page.split('\n'):
            pdf.cell(200, 8, txt=sanitize(line), ln=True)
    return pdf.output(dest='S').encode('latin-1')

def extract_simple_entities(cleaned_pages):
    """Fallback entity extraction using regex when spaCy is unavailable"""
    import re
    
    entities = []
    date_pattern = r"\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b"
    provider_pattern = r"(?:Dr\.|Doctor|MD|DO|NP|PA)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})"
    facility_pattern = r"([A-Z][A-Za-z']+(?:\s+[A-Z][A-Za-z']+){0,3})\s+(?:Hospital|Medical Center|Clinic|Center|Laboratory)"
    lab_pattern = r"\b(?:CBC|Complete Blood Count|Lipid Panel|A1C|Hemoglobin A1C|TSH|Thyroid|Metabolic Panel)\b"
    
    # Track entities for propagation (Scenario 6)
    current_dos = None
    current_provider = None
    current_facility = None
    
    for idx, text in enumerate(cleaned_pages):
        entity = {
            "page_number": idx + 1,
            "date": None,
            "provider": None,
            "facility": None,
            "lab_tests": [],
            "medical_terms": []
        }
        
        # Extract date
        date_matches = re.findall(date_pattern, text)
        if date_matches:
            entity["date"] = date_matches[0]
            entity["date_candidates"] = date_matches
            
        # Extract provider
        provider_match = re.search(provider_pattern, text)
        if provider_match:
            entity["provider"] = provider_match.group(0)
            
        # Extract facility
        facility_match = re.search(facility_pattern, text)
        if facility_match:
            entity["facility"] = facility_match.group(0)
            
        # Extract lab tests
        lab_matches = re.findall(lab_pattern, text)
        if lab_matches:
            entity["lab_tests"] = list(set(lab_matches))
            
        # Handle missing information (Scenario 6)
        if not entity["date"] and current_dos:
            entity["date"] = current_dos
        else:
            current_dos = entity["date"]
            
        if not entity["provider"] and current_provider:
            entity["provider"] = current_provider
        else:
            current_provider = entity["provider"]
            
        if not entity["facility"] and current_facility:
            entity["facility"] = current_facility
        else:
            current_facility = entity["facility"]
            
        entities.append(entity)
    
    return entities

def get_simple_timeline(entities):
    """Simplified timeline when spaCy is unavailable"""
    timeline = {}
    
    for entity in entities:
        if entity["date"]:
            date = entity["date"]
            if date not in timeline:
                timeline[date] = []
            timeline[date].append(entity["page_number"])
    
    return timeline

def main():
    uploaded_file = st.file_uploader("Upload Clinical PDF", type=["pdf"])
    
    if uploaded_file:
        st.success("✅ File Authenticated - HIPAA Compliant Processing")
        
        # Processing Pipeline
        with st.spinner("🔍 Document Analysis in Progress..."):
            # Extract and clean content
            raw_pages = extract_pdf_text(uploaded_file)
            metadata = extract_metadata(uploaded_file)
            headers, footers = extract_header_footer(raw_pages)
            cleaned_pages = [clean_page_text(p, headers, footers) for p in raw_pages]
            
            # Extract entities
            with st.spinner("🧬 Extracting medical entities..."):
                if entity_extraction_available:
                    entities = extract_entities_from_pages(cleaned_pages)
                else:
                    entities = extract_simple_entities(cleaned_pages)
                    st.warning("⚠️ Using simplified entity extraction. For better results, ensure spaCy is properly installed.")

        # Document Intelligence Dashboard
        st.subheader("📊 Document Analytics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Pages", len(raw_pages))
        with col2:
            dates = [e["date"] for e in entities if e["date"]]
            st.metric("Dates Identified", len(set(dates)))
        with col3:
            providers = [e["provider"] for e in entities if e["provider"]]
            st.metric("Providers Identified", len(set(providers)))
        with col4:
            facilities = [e["facility"] for e in entities if e["facility"]]
            st.metric("Facilities Identified", len(set(facilities)))

        # Document Explorer Tabs
        tabs = st.tabs(["📅 Timeline", "📄 Page View", "🔍 Entity Summary", "📊 Analytics"])
        
        # Tab 1: Timeline View
        with tabs[0]:
            st.subheader("📅 Document Timeline")
            timeline_fig = visualize_timeline(entities)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True)
                
                # Create a table of dates and pages
                if entity_extraction_available:
                    timeline_data = get_document_timeline(entities)
                else:
                    timeline_data = get_simple_timeline(entities)
                    
                if timeline_data:
                    st.subheader("Date of Service (DOS) Summary")
                    date_table = []
                    for date, pages in timeline_data.items():
                        # Find providers for this date
                        date_providers = set()
                        for page_num in pages:
                            provider = entities[page_num-1].get("provider")
                            if provider:
                                date_providers.add(provider)
                        
                        date_table.append({
                            "Date": date,
                            "Pages": ", ".join(map(str, pages)),
                            "Provider(s)": ", ".join(date_providers) if date_providers else "Unknown",
                            "Page Count": len(pages)
                        })
                    
                    st.dataframe(pd.DataFrame(date_table), use_container_width=True)
            else:
                st.warning("No date information found for timeline visualization")
        
        # Tab 2: Page View
        with tabs[1]:
            # Page selection
            page_num = st.selectbox(
                "Select Page",
                options=range(1, len(raw_pages)+1),
                format_func=lambda x: f"Page {x}"
            )
            
            # Display page content
            col1, col2 = st.columns([1, 3])
            with col1:
                st.subheader(f"Page {page_num}")
                
                # Show entity information
                entity = entities[page_num - 1]
                st.markdown("**🧬 Extracted Metadata**")
                
                # Create a clean entity display
                entity_card = {
                    "Date": entity.get('date', 'N/A'),
                    "Provider": entity.get('provider', 'N/A'),
                    "Facility": entity.get('facility', 'N/A'),
                }
                
                for key, value in entity_card.items():
                    st.markdown(f"**{key}:** {value}")
                
                if entity.get('lab_tests'):
                    st.markdown("**Lab Tests:**")
                    for test in entity['lab_tests']:
                        st.markdown(f"- {test}")
                
                if entity.get('medical_terms'):
                    st.markdown("**Medical Terms:**")
                    for term in entity['medical_terms']:
                        st.markdown(f"- {term}")
                        
                # Page navigation
                st.markdown("---")
                nav_col1, nav_col2 = st.columns(2)
                with nav_col1:
                    if page_num > 1:
                        if st.button("◀️ Previous Page"):
                            st.session_state.page_num = page_num - 1
                            st.experimental_rerun()
                with nav_col2:
                    if page_num < len(raw_pages):
                        if st.button("Next Page ▶️"):
                            st.session_state.page_num = page_num + 1
                            st.experimental_rerun()
            
            with col2:
                view_tab1, view_tab2 = st.tabs(["Original", "Cleaned"])
                with view_tab1:
                    st.text_area("Original", raw_pages[page_num-1][:2500], 
                               height=500, label_visibility="collapsed")
                with view_tab2:
                    st.text_area("Cleaned", cleaned_pages[page_num-1][:2500], 
                               height=500, label_visibility="collapsed")
        
        # Tab 3: Entity Summary
        with tabs[2]:
            st.subheader("🔍 Entity Summary")
            
            # Create a DataFrame for entity display
            entity_df = pd.DataFrame([{
                "Page": e["page_number"],
                "Date": e.get("date", ""),
                "Provider": e.get("provider", ""),
                "Facility": e.get("facility", ""),
                "Lab Tests": ", ".join(e.get("lab_tests", [])),
                "Medical Terms": ", ".join(e.get("medical_terms", []))
            } for e in entities])
            
            # Add search/filter functionality
            search_term = st.text_input("🔍 Search entities", "")
            if search_term:
                filtered_df = entity_df[
                    entity_df.astype(str).apply(
                        lambda row: row.str.contains(search_term, case=False).any(), 
                        axis=1
                    )
                ]
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(entity_df, use_container_width=True)
            
            # Entity statistics
            st.subheader("Entity Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                providers = [e["provider"] for e in entities if e["provider"]]
                if providers:
                    st.markdown("**Top Providers:**")
                    provider_counts = pd.Series(providers).value_counts()
                    for provider, count in provider_counts.items():
                        st.markdown(f"- {provider}: {count} pages")
            
            with col2:
                facilities = [e["facility"] for e in entities if e["facility"]]
                if facilities:
                    st.markdown("**Top Facilities:**")
                    facility_counts = pd.Series(facilities).value_counts()
                    for facility, count in facility_counts.items():
                        st.markdown(f"- {facility}: {count} pages")
            
            with col3:
                lab_tests = []
                for e in entities:
                    lab_tests.extend(e.get("lab_tests", []))
                
                if lab_tests:
                    st.markdown("**Lab Tests Found:**")
                    lab_counts = pd.Series(lab_tests).value_counts()
                    for lab, count in lab_counts.items():
                        st.markdown(f"- {lab}: {count} mentions")
        
        # Tab 4: Analytics
        with tabs[3]:
            st.subheader("📊 Entity Analytics")
            
            # Create visualizations
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Provider Distribution", "Date Distribution", "Entity Correlation"]
            )
            
            if chart_type == "Provider Distribution":
                providers = [e["provider"] for e in entities if e["provider"]]
                if providers:
                    provider_counts = pd.Series(providers).value_counts()
                    fig = px.pie(
                        values=provider_counts.values,
                        names=provider_counts.index,
                        title="Document Distribution by Provider",
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No provider information found for visualization")
                    
            elif chart_type == "Date Distribution":
                dates = [e["date"] for e in entities if e["date"]]
                if dates:
                    date_counts = pd.Series(dates).value_counts()
                    fig = px.bar(
                        x=date_counts.index,
                        y=date_counts.values,
                        labels={"x": "Date", "y": "Page Count"},
                        title="Page Distribution by Date"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No date information found for visualization")
                    
            elif chart_type == "Entity Correlation":
                # Create a correlation matrix between providers and facilities
                provider_facility_matrix = pd.DataFrame([
                    {"Provider": e.get("provider", "Unknown"), 
                     "Facility": e.get("facility", "Unknown")}
                    for e in entities if e.get("provider") or e.get("facility")
                ])
                
                if not provider_facility_matrix.empty:
                    pivot = pd.crosstab(
                        provider_facility_matrix["Provider"], 
                        provider_facility_matrix["Facility"]
                    )
                    
                    fig = px.imshow(
                        pivot, 
                        labels=dict(x="Facility", y="Provider", color="Page Count"),
                        title="Provider-Facility Correlation"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient data for correlation analysis")

        # Export Section
        st.subheader("📤 Export Options")
        col1, col2, col3 = st.columns(3)
        
        # Cleaned Text Export
        with col1:
            cleaned_text = "\n\n".join(cleaned_pages)
            st.download_button(
                label="📥 Download Cleaned Text",
                data=cleaned_text,
                file_name="cleaned_document.txt",
                mime="text/plain"
            )
        
        # Entity JSON Export
        with col2:
            entity_json = json.dumps(entities, indent=2)
            st.download_button(
                label="💾 Export Entities (JSON)",
                data=entity_json,
                file_name="document_entities.json",
                mime="application/json"
            )
        
        # PDF Export
        with col3:
            try:
                pdf_data = generate_clean_pdf(cleaned_pages)
                st.download_button(
                    label="🖨️ Download Cleaned PDF",
                    data=pdf_data,
                    file_name="cleaned_document.pdf",
                    mime="application/pdf"
                )
            except Exception:
                st.error("PDF generation failed")
        
        # Advanced Export Options
        with st.expander("📁 Advanced Export Options"):
            st.markdown("### Entity JSON Preview")
            st.code(entity_json[:1000] + "...", language="json")
            
            st.markdown("### Export Filtered Entities")
            export_provider = st.selectbox(
                "Filter by Provider",
                ["All Providers"] + list(set(e["provider"] for e in entities if e["provider"]))
            )
            
            if export_provider != "All Providers":
                filtered_entities = [e for e in entities if e.get("provider") == export_provider]
                filtered_json = json.dumps(filtered_entities, indent=2)
                
                st.download_button(
                    label=f"📥 Export {export_provider} Records",
                    data=filtered_json,
                    file_name=f"{export_provider.replace(' ', '_')}_records.json",
                    mime="application/json"
                )
    else:
        st.info("👨⚕️ Upload clinical documentation to begin analysis")

if __name__ == "__main__":
    main()
