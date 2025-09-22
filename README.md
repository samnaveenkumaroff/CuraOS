
# CuraOS

[![Python Version](https://img.shields.io/badge/python–3.9–blue.svg)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)  
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)


![CuraOS](https://github.com/user-attachments/assets/37917554-6c92-4177-b9d8-b90f28958444)

CuraOS is a fully modular, AI-powered pipeline that automates the transformation of unstructured multi-page medical records (PDFs, scanned documents) into structured and actionable electronic health records (EHRs). The system handles every aspect of preprocessing, including segmentation, clustering, de-identification, metadata extraction, and interactive visualization. CuraOS
#EHR

---


## 📋 Table of Contents

1. [Summary](#1-summary)  
2. [Introduction](#2-introduction)  
3. [Problem Statement](#3-problem-statement)  
4. [Key Features](#4-key-features)  
5. [Competitive Landscape](#5-competitive-landscape)  
6. [Adoption Insights](#6-adoption-insights)  
7. [Architecture](#7-architecture)  
8. [Installation](#8-installation)  
9. [Pipeline Components](#9-pipeline-components)  
10. [Setup Scripts](#10-setup-scripts)  
11. [Usage](#11-usage)  
12. [How CuraOS Excels](#12-how-curaos-excels)  
13. [Output Formats](#13-output-formats)  
14. [Contributing](#14-contributing)  
15. [License](#15-license)  

---

## 1. Summary

CuraOS is a healthcare data pipeline that takes raw, unstructured clinical documents and converts them into clean, structured, de-identified records with enhanced metadata—enabling advanced analytics, research, and integration with hospital systems.

---

## 2. Introduction

Electronic Health Records are foundational to modern healthcare—but much of a patient's history remains buried in unstructured documents. CuraOS helps organizations convert paper-based or scanned records into usable, analyzable formats—without compromising data security or compliance.

---

## 3. Problem Statements Tackled

- **Data trapped in PDFs and scans**
- **Manual data entry is costly and error-prone**
- **Lack of compliance without proper de-identification**
- **Standard tools don’t support page-level granularity**

---

## 4. Key Features

- ✅ HIPAA-compliant PHI de-identification  
- 🧠 Entity extraction: Dates, doctors, labs, conditions  
- 📑 Page-wise semantic clustering using HDBSCAN + embeddings  
- 📈 Timeline generation for easy record navigation  
- 🖼️ Interactive dashboards for data visualization  
- 🧰 Export options: CSV, JSON, FHIR, PDFs, cleaned text  
- 🔌 Modular design to integrate custom OCR/NLP tools  
- 🌐 Supports English and regional languages  

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

CuraOS can be adopted by:

- 📊 **Hospitals & Clinics** for digitizing historical patient records  
- 🏥 **EHR Platforms** (Epic, HealthPlix, Jio Health, etc.) for document enrichment  
- 🔬 **Research Labs** that require clean, anonymized medical data  
- 🧪 **Pharma/Insurance** companies for large-scale data extraction & compliance  

---

## 7. Architecture

### 7.1 High-Level Architecture

![Architecture](https://github.com/user-attachments/assets/c2069e2d-6542-403e-b390-e486be0ea5ab)

**Modules:**

1. **Input Handler**  
   - Accepts PDFs, scanned images, or JSONs.  

2. **Preprocessing**  
   - Header/footer removal  
   - OCR if scanned  

3. **Entity Extraction**  
   - Using spaCy and regex patterns  

4. **De-identification**  
   - Redacts PHI like names, MRNs, phone numbers  

5. **Feature Engineering + Clustering**  
   - Embeddings (S-BERT / MiniLM)  
   - Clustering using HDBSCAN  

6. **Timeline & Visualization**  
   - Interactive dashboard with analytics  

7. **Multi-format Export**  
   - Cleaned files in multiple formats  

---

### 7.2 Workflow Diagram

![Workflow](https://github.com/user-attachments/assets/79465b2f-2c50-4515-9288-70e215692e03)

**Process Flow:**

- Users upload bulk documents  
- Files are preprocessed (OCR + cleanup)  
- Metadata and entities are extracted  
- Pages are clustered into logical documents  
- PHI is redacted and visualization generated  
- Exports are generated for downstream use  

---

## 8. Installation

### Prerequisites

- Python 3.9  
- Git  
- Conda (recommended) or virtualenv  
- Compatible with Linux, macOS, and Windows  

### Clone Repository

```bash
git clone https://github.com/samnaveenkumaroff/CuraOS.git
cd CuraOS
````

### Create Virtual Environment

**Using Conda (Recommended):**

```bash
conda create -y -n curaos_env python=3.9
conda activate curaos_env
```

**Using virtualenv (Alternative):**

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 9. Pipeline Components

1. **Document Ingestion**

   * Upload via UI or API
   * Accepts PDFs, scanned TIFFs, and JSON

2. **Preprocessing**

   * Text cleanup, OCR via Tesseract
   * Removes headers, footers, duplicates

3. **De-identification**

   * Custom rules + regex to mask PHI

4. **Entity Extraction**

   * Dates, provider names, locations, labs

5. **Clustering**

   * Page embeddings via SciBERT or MiniLM
   * HDBSCAN for document-level grouping

6. **Timeline & Summary Generation**

   * Per-patient history timeline
   * Entity summary and distribution charts

7. **Export & Integration**

   * Formats: CSV, PDF, TXT, FHIR JSON
   * Easily integrable with existing systems

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

echo "✅ Setup complete. Run the app with:"
echo "streamlit run path/app_pdf_csv.py"
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

echo ✅ Setup complete. Run the app with:
echo streamlit run path/app_pdf_csv.py
pause
```

---

## 11. Usage

After installation and environment activation:

### 1. Launch the Streamlit Dashboard

```bash
streamlit run path/app_pdf_csv.py
```

Explore:

* 📆 Patient Timeline
* 📄 Page View for clustered documents
* 🧠 Entity Summary & Statistics
* 📤 Export Cleaned Files

### 2. CLI Option (if implemented)

```bash
python run_pipeline.py --input ./data/sample.pdf --output-dir ./results
```

---

## 12. How CuraOS Excels

* ✅ Granular page-wise segmentation
* 🧩 Modular NLP engine
* 🔐 Built-in de-identification
* 🖼️ Visual analytics for rapid insight
* 🔄 Export-ready formats for EHR integration

---

## 13. Output Formats

* `.txt`: Cleaned text
* `.pdf`: Sanitized, de-identified PDFs
* `.csv`: Structured data tables
* `.json`: Raw and enriched data
* `.fhir.json`: Compatible with healthcare standards
* `.html`: Embedded dashboards

---

## 14. Contributing

Contributions are welcome!

1. Fork this repo
2. Create your branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m "Feature: YourFeature"`)
4. Push (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 15. License

This project is licensed under the [MIT License](LICENSE).
Made with Love by Sam Naveenkumar V
([samnaveenkumaroff](https://in.linkedin.com/in/samnaveenkumaroff))

---

**CuraOS — From Paper to Patient Insight.**

