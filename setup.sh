#!/bin/bash

# -------------------------------
# MRRM_Project Setup for Linux/macOS
# Project Repo: https://github.com/samnaveenkumaroff/CuraOS
# Conda Env: CuraOS
# -------------------------------

set -e  # Exit immediately on any error

echo "📦 MRRM_Project Setup Started..."

# 1. Clone GitHub Repo if not exists
if [ ! -d "CuraOS" ]; then
  echo "📥 Cloning CuraOS GitHub repository..."
  git clone https://github.com/samnaveenkumaroff/CuraOS.git || {
    echo "❌ Git clone failed. Check internet connection or Git install."
    exit 1
  }
else
  echo "✅ CuraOS directory already exists. Skipping git clone."
fi

cd CuraOS

# 2. Create Conda environment
echo "🐍 Creating Conda environment: CuraOS (Python 3.10)..."
conda create -n CuraOS python=3.10 -y || {
  echo "❌ Conda environment creation failed."
  exit 1
}

# 3. Activate the environment
echo "🔁 Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate CuraOS

# 4. Install dependencies
echo "📄 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Streamlit Theme Config (Optional)
echo "🎨 Setting up Streamlit theme config..."
mkdir -p ~/.streamlit
cat <<EOF > ~/.streamlit/config.toml
[theme]
base="light"
primaryColor="#4CAF50"
backgroundColor="#F5F5F5"
secondaryBackgroundColor="#E0E0E0"
textColor="#000000"
EOF

# 6. Launch Streamlit App
echo "🚀 Launching Streamlit App: outputs/app_pdf_csv.py"
streamlit run outputs/app_pdf_csv.py
