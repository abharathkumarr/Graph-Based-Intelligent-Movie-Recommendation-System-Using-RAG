# Usage Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))
- 8GB+ RAM recommended (for loading embeddings)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG.git
   cd Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_ui.txt
   ```

3. **Set your Groq API key**
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

4. **Launch the application**
   ```bash
   ./run_app.sh
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8502`

## Example Queries

Try these queries to explore the system:

- **Rating-based**: "Find movies with rating above 8.0"
- **Genre + Year**: "List adventure movies released after 2010"  
- **Actor-based**: "Movies acted by Leonardo DiCaprio"
- **Multiple filters**: "Comedy movies produced in USA with budget over $50M"
- **Director-based**: "Movies directed by Steven Spielberg"
- **Genre exploration**: "Recent movies in Adventure genre"

## Tips for Best Results

1. **Be specific**: Include details like ratings, years, genres
2. **Combine filters**: Mix multiple criteria for refined results
3. **Use natural language**: No need for formal syntax
4. **Check response time**: Most queries complete in 2-3 seconds

## Troubleshooting

**Issue**: "Model files not found"  
**Solution**: Ensure `triplet_sentences.pkl` and `triplet_embeddings.pkl` are in the root directory

**Issue**: "API key error"  
**Solution**: Verify your Groq API key is set correctly with `echo $GROQ_API_KEY`

**Issue**: "Out of memory"  
**Solution**: Close other applications or use a machine with more RAM

**Issue**: "Slow loading"  
**Solution**: First load takes ~30 seconds to load 337MB embeddings (cached afterwards)

## Running the Jupyter Notebook

To reproduce the entire pipeline from scratch:

1. Open `CMPE258_Project_Code.ipynb` in Jupyter or Google Colab
2. Set up Neo4j database connection (or use existing data)
3. Run cells sequentially to:
   - Extract knowledge triplets
   - Generate embeddings
   - Build FAISS index
   - Test RAG pipeline
   - Save model files

## Development

To modify the UI:
1. Edit `app_full.py`
2. Restart the Streamlit app (Ctrl+C then `./run_app.sh`)
3. Changes will auto-reload in development mode

## Support

For issues or questions:
- Open an issue on GitHub
- Contact: bharathkumar.a@sjsu.edu
