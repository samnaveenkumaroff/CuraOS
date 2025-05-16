````markdown
# CuraOS

[![Python Version](https://img.shields.io/badge/python–3.9–blue.svg)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)  
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

A fully modular, AI-powered pipeline that automates the segmentation, de-identification, and clustering of unstructured multi-page medical records into organized electronic health records (EHRs). CuraOS streamlines the transformation of diverse clinical documents into structured, actionable formats—ensuring data privacy, HIPAA compliance, and adaptability to any healthcare environment.

---

## 📋 Table of Contents

1. [Summary](#1-summary)  
2. [Introduction](#2-introduction)  
3. [Problem Statement](#3-problem-statement)  
4. [Key Features](#4-key-features)  
5. [Competitive Landscape](#5-competitive-landscape)  
6. [Adoption Insights](#6-adoption-insights)  
7. [Architecture](#7-architecture)  
   - [7.1 Architecture Diagram](#71-architecture-diagram)  
   - [7.2 Workflow Diagram](#72-workflow-diagram)  
8. [Pipeline Components](#8-pipeline-components)  
9. [Installation](#9-installation)  
10. [Setup Scripts](#10-setup-scripts)  
11. [Usage](#11-usage)  
12. [How CuraOS Excels](#12-how-curaos-excels)  
13. [Output Formats](#13-output-formats)  
14. [Contributing](#14-contributing)  
15. [License](#15-license)  

---

## 1. Summary

CuraOS is an AI-driven, modular pipeline that converts unstructured medical PDFs and scanned images into structured EHRs. It automates:

- **Segmentation & Clustering** of related pages  
- **De-identification** (automatic PHI redaction)  
- **Metadata Extraction** (dates, providers, facilities)  
- **Visualization & Export** (CSV, JSON, FHIR, dashboards)  

Designed for on-premise or cloud deployment, CuraOS is lightweight, API-driven, and easily extensible to regional languages.

---

## 2. Introduction

Electronic Health Records (EHRs) have transformed patient care by digitizing data. Yet, most clinical documents remain locked in unstructured PDFs or scanned images—hindering analytics, research, and interoperability under HIPAA regulations. CuraOS addresses this gap by providing page-level AI tools to ingest, clean, extract, cluster, and export medical records.

---

## 3. Problem Statement

- **Fragmented Records**: Clinical data spread across multiple pages and document types.  
- **Manual Overhead**: Time-consuming, error-prone manual processing.  
- **Regulatory Pressure**: Need for automated HIPAA-compliant de-identification.  
- **Lack of Granularity**: Existing EHR systems process documents as monoliths, not page by page.

---

## 4. Key Features

- 🔒 **Data Privacy & De-identification**  
- 📄 **PDF & OCR Processing** with header/footer cleanup  
- 🧬 **Entity Extraction** (dates, providers, facilities, lab tests, medical terms)  
- 📊 **Interactive Dashboard** (timeline, entity summary, analytics)  
- 🔗 **Page-wise Clustering** via HDBSCAN + S-BERT embeddings  
- 🔄 **Carry-Forward Logic** to fill missing metadata  
- 💾 **Multi-format Exports** (CSV, JSON, FHIR, cleaned PDF, cleaned text)  
- ⚙️ **Modular Design** for easy swapping of OCR, NER, clustering components  
- 🌐 **Platform Independent**: Windows, macOS, Linux, Docker  

---

## 5. Competitive Landscape

| Solution           | Page-wise Clustering | Modular NLP Pipeline | On-Premise | Regional Language Support |
|--------------------|:--------------------:|:--------------------:|:----------:|:-------------------------:|
| **CuraOS**         | ✅                   | ✅                   | ✅         | ✅                        |
| Carta Healthcare   | ❌                   | ✅                   | ❌         | ❌                        |
| Flatiron Health    | ❌                   | ✅                   | ❌         | ❌                        |
| Komodo Health      | ❌                   | ✅                   | ❌         | ❌                        |

---

## 6. Adoption Insights

- **U.S. Leaders**: Epic, Oracle Health, Meditech, NextGen  
- **Indian Innovators**: Eka Care, HealthPlix, Docpulse, Healthray, Jio KiviHealth  
- **Opportunity**: CuraOS enhances existing platforms by adding fine-grained, AI-driven document clustering and de-identification—critical for cost-sensitive and diverse healthcare settings.

---

## 7. Architecture

```text
┌────────┐    ┌───────────┐    ┌─────────────────┐    ┌─────────────────────┐    ┌───────┐
│ Input  │───▶│ Preprocess│───▶│ Entity Extraction│───▶│ Data Aggregation &  │───▶│ Export │
│ (PDF/JSON)  │   │ (OCR,     │   │ (spaCy & Regex)  │   │ Visualization       │   │       │
│             │   │ clean-up) │   └─────────────────┘   │ (timelines, charts) │   │       │
└────────┘    └───────────┘                         └─────────────────────┘    └───────┘
````

### 7.1 Architecture Diagram

Below is a high-level visual representation of CuraOS’s modular architecture, showing how data flows through each block from ingestion to export.

![Architecture Diagram](https://github.com/user-attachments/assets/c2069e2d-6542-403e-b390-e486be0ea5ab)

### 7.2 Workflow Diagram

This diagram illustrates the end-to-end workflow: from uploading raw medical documents, through preprocessing, entity extraction, clustering, and finally to multi-format export and visualization.

![Workflow Diagram](https://github.com/user-attachments/assets/79465b2f-2c50-4515-9288-70e215692e03)

---

## 8. Pipeline Components

1. **Data Ingestion**

   * Bulk upload via Web UI or API
2. **Preprocessing & De-identification**

   * PDF parsing, OCR (scanned images), header/footer removal
   * PHI redaction for HIPAA compliance
3. **Feature Engineering & Clustering**

   * Metadata extraction (dates, providers, facilities)
   * Semantic embeddings (SciBERT or MiniLM)
   * Density-based clustering (HDBSCAN) with auto-labeling
4. **Aggregation & Visualization**

   * Timeline view, entity summary, analytics charts (Plotly)
5. **Export**

   * Cleaned text (.txt), sanitized PDF (.pdf)
   * CSV exports: simple, detailed, filtered, timeline, lab tests
   * JSON & FHIR outputs for EHR interoperability

---

## 9. Installation

### Prerequisites

* Python 3.9+
* [Conda](https://docs.conda.io/) (optional, but recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CuraOS.git
cd CuraOS
```

### 2. Create & Activate Environment

**Conda** (recommended):

```bash
conda create -y -n curaos_env python=3.9
conda activate curaos_env
```

**Or** virtualenv:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

## 10. Setup Scripts

### `setup.sh` (macOS/Linux)

```bash
#!/usr/bin/env bash
echo "❯ Creating Conda environment 'curaos_env'..."
conda create -y -n curaos_env python=3.9

echo "❯ Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate curaos_env

echo "❯ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "❯ Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete. Run 'conda activate curaos_env' to begin."
```

Make it executable:

```bash
chmod +x setup.sh
```

Run:

```bash
./setup.sh
```

---

### `setup.bat` (Windows)

```bat
@echo off
echo ❯ Creating Conda environment 'curaos_env'...
conda create -y -n curaos_env python=3.9

echo ❯ Activating environment...
call conda activate curaos_env

echo ❯ Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo ❯ Downloading spaCy model...
python -m spacy download en_core_web_sm

echo ✅ Setup complete. Run 'conda activate curaos_env' to begin.
pause
```

Double-click or run:

```cmd
setup.bat
```

---

## 11. Usage

After setup and activation:

```bash
# Run the Streamlit dashboard
streamlit run app.py

# Or run full pipeline via CLI (if provided)
python run_pipeline.py --input path/to/your/file.pdf --output-dir ./results
```

Explore interactive tabs:

* Timeline
* Page View
* Entity Summary
* Entity Analytics
* CSV & PDF Exports

---

## 12. How CuraOS Excels

* **Page-wise Granularity**: Finer organization than whole-document approaches
* **Modular NLP Pipeline**: Swap OCR, NER, clustering components easily
* **Adaptability**: On-premise deployment; supports regional languages
* **Open & Extensible**: API-driven; integrate with any EHR or research tool
* **Output Flexibility**: JSON, CSV, FHIR, PDF, Text & dashboards

---

## 13. Output Formats

* **Cleaned Text** (`.txt`)
* **Sanitized PDF** (`.pdf`)
* **CSV Exports**:

  * Simple
  * Detailed
  * Filtered
  * Timeline
  * Lab Tests
* **JSON & FHIR** for EHR interoperability
* **Interactive Dashboards** (Streamlit + Plotly)

---

## 14. Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 15. License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

**Enjoy CuraOS!**
Transform your unstructured medical records into actionable EHR data—securely, reliably, and at scale.

```
```
