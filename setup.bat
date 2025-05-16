@echo off
SETLOCAL

:: -----------------------------
:: MRRM_Project Setup for Windows
:: GitHub: CuraOS by @samnaveenkumaroff
:: -----------------------------

:: Step 1: Clone GitHub repo if folder doesn't exist
IF NOT EXIST "CuraOS" (
    echo [📥] Cloning CuraOS project from GitHub...
    git clone https://github.com/samnaveenkumaroff/CuraOS.git
    IF ERRORLEVEL 1 (
        echo [❌] Git clone failed. Check your internet or Git install.
        EXIT /B 1
    )
) ELSE (
    echo [✅] CuraOS folder already exists. Skipping clone.
)

:: Step 2: Navigate to project directory
cd CuraOS

:: Step 3: Create Conda Environment
echo [📦] Creating Conda environment: CuraOS (Python 3.10)...
conda create -n CuraOS python=3.10 -y
IF ERRORLEVEL 1 (
    echo [❌] Failed to create Conda environment.
    EXIT /B 1
)

:: Step 4: Activate Environment
CALL conda activate CuraOS

:: Step 5: Install Dependencies
echo [📄] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Step 6: (Optional) Check for Tesseract OCR
where tesseract >nul 2>nul
IF ERRORLEVEL 1 (
    echo [⚠️] Tesseract not found. Please install Tesseract from:
    echo     https://github.com/tesseract-ocr/tesseract#windows
) ELSE (
    echo [✅] Tesseract is installed.
)

:: Step 7: Launch Streamlit App
echo [🚀] Launching Streamlit App: outputs/app_pdf_csv.py...
streamlit run outputs/app_pdf_csv.py

ENDLOCAL
