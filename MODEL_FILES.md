# Model Files

## Required Files

The RAG system requires two large model files that exceed GitHub's 100MB size limit:

1. **`triplet_sentences.pkl`** (9.3 MB) - 229,894 knowledge triplets in natural language
2. **`triplet_embeddings.pkl`** (337 MB) - 384-dimensional embeddings for semantic search

## How to Obtain These Files

### Option 1: Generate from Notebook (Recommended)

Run the Jupyter notebook to generate these files yourself:

1. Open `CMPE258_Project_Code.ipynb` in Google Colab or local Jupyter
2. Set up Neo4j database connection (credentials provided in notebook)
3. Execute all cells sequentially:
   - Extract knowledge triplets from Neo4j
   - Generate embeddings using SentenceTransformers  
   - Save to pickle files
4. Download the generated `.pkl` files and place them in the project root directory

### Option 2: Request from Team

Contact any team member to obtain the pre-generated files:

- **Bharath Kumar A**: bharathkumar.a@sjsu.edu
- **Saripella Sriyavarma**: sriyavarma.saripella@sjsu.edu  
- **Venkata Siva Sai Krishna Prasad Y**: venkatasivasaikrishnaprasad.yedupati@sjsu.edu

### Option 3: Alternative Hosting

The files may be hosted on cloud storage platforms. Check the GitHub repository's Releases section for download links.

## File Verification

After obtaining the files, verify they are correct:

```bash
ls -lh triplet_*.pkl
```

Expected output:
```
-rw-r--r--  1 user  staff   337M  triplet_embeddings.pkl
-rw-r--r--  1 user  staff   9.3M  triplet_sentences.pkl
```

## Quick Test

Verify the files load correctly:

```python
import pickle

# Test loading
with open('triplet_sentences.pkl', 'rb') as f:
    sentences = pickle.load(f)
    print(f"Loaded {len(sentences):,} sentences")  # Should be 229,894

with open('triplet_embeddings.pkl', 'rb') as f:
    embeddings = pickle.load(f)
    print(f"Embeddings shape: {embeddings.shape}")  # Should be (229894, 384)
```

## Important Notes

- These files are required for the Streamlit UI to work
- Place them in the **project root directory** (same level as `app_full.py`)
- The first load takes ~30 seconds due to file size
- Subsequent loads are cached by Streamlit for faster access

## File Size Warning

GitHub has a 100MB file size limit. These files are intentionally excluded from version control via `.gitignore` to comply with GitHub's policies.
