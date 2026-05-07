#!/bin/bash

# Quick Launcher for Movie Recommendation UI
echo "🎬 Movie Recommendation System - Quick Start"
echo "============================================"
echo ""

# Check if pickle files exist
if [ ! -f "triplet_sentences.pkl" ] || [ ! -f "triplet_embeddings.pkl" ]; then
    echo "❌ ERROR: Model data files not found!"
    echo ""
    echo "Please do the following:"
    echo "1. Open your Colab notebook"
    echo "2. Copy the code from SAVE_IN_COLAB.py"
    echo "3. Add it as a new cell at the END of your notebook"
    echo "4. Run the cell"
    echo "5. Download both .pkl files"
    echo "6. Move them to this folder"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "✅ Found model data files"
echo ""

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Installing dependencies..."
    pip3 install -r requirements_ui.txt
fi

echo "✅ Dependencies ready"
echo ""

# Launch the app
echo "🚀 Launching Streamlit app..."
echo ""
echo "👉 The app will open in your browser"
echo "👉 Enter your API key in the sidebar"
echo "👉 Press Ctrl+C to stop the server"
echo ""

streamlit run app_full.py
