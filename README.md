# Graph-Based Intelligent Movie Recommendation System Using RAG

> **Course:** CMPE 258 - Deep Learning (Spring 2026)  
> **Group:** 19  
> **GitHub:** [Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG](https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG)

## Team Members

| Name | Student ID | Email |
|------|------------|-------|
| Bharath Kumar A | 018221268 | bharathkumar.a@sjsu.edu |
| Saripella Sriyavarma | 019130553 | sriyavarma.saripella@sjsu.edu |
| Venkata Siva Sai Krishna Prasad Y | 018320835 | venkatasivasaikrishnaprasad.yedupati@sjsu.edu |

---

##  Motivation

Traditional recommendation systems rely heavily on collaborative or content-based filtering, which often fail to capture deeper relationships between entities. This project aims to **enhance movie recommendations** using:
- **Knowledge Graphs (KGs)** to model semantic connections
- **Retrieval-Augmented Generation (RAG)** to provide interpretable, grounded responses using LLMs

---

## Architecture

![Pipeline](pipeline.png)

---

## Dataset

- Source: [Neo4j “recommendations” dataset](https://github.com/neo4j-graph-examples/recommendations)
- Entities & Relationships:
  - `(:Movie)-[:IN_GENRE]->(:Genre)`
  - `(:User)-[:RATED]->(:Movie)`
  - `(:Actor)-[:ACTED_IN]->(:Movie)`
  - `(:Director)-[:DIRECTED]->(:Movie)`
- **Nodes**: 28,865  
- **Edges**: 166,262

---

##  Methodology

### 1. Knowledge Triplet Construction
- Extract triplets from Neo4j and convert them into human-readable format:
  ```
  {'movie': 'Toy Story', released: 1995} → "Toy Story was released in year 1995"
  ```
- Total Sentences: **229,894**

### 2.  Embedding Generation
- Use HuggingFace **SentenceTransformers** (MiniLM) to embed triplets into 384-d vector space.

### 3.  FAISS Indexing
- Index embeddings using **FAISS** (L2 distance).
- Enables fast top-k retrieval during inference.

### 4.  Cosine Reranking
- Use cosine similarity to improve retrieval precision after FAISS.

### 5.  Retrieval-Augmented Generation (RAG)
- Use **Groq-hosted LLaMA3-70B-8192** with LangChain:
  1. Retrieve relevant triplets
  2. Format into a prompt
  3. Send to LLM for response generation

### 6. Evaluation
- **Precision** = Correct retrieved / Total retrieved  
- **Recall** = Correct retrieved / Total relevant  
- **F1 Score** = Harmonic mean of Precision and Recall

---

## Results

- High-quality movie recommendations that are **fact-grounded** and **interpretable**
- Retrieval results match Neo4j Cypher query outputs
- Enhanced relevance via RAG pipeline

### Evaluation Metrics

**Overall RAG System Performance:**
- Average Precision@10: **0.65**
- Average Recall@10: **0.26**
- Average F1-score@10: **0.30**

---

## Progress Update

### Completed

✅ **Data Extraction & Processing**
- Successfully extracted 229,894 knowledge triplets from Neo4j database
- Converted graph relationships into natural language sentences
- Processed all movie, actor, director, genre, and user rating entities

✅ **Embedding & Indexing**
- Generated 384-dimensional embeddings using SentenceTransformers (all-MiniLM-L6-v2)
- Built FAISS index with L2 distance for efficient similarity search
- Implemented cosine similarity re-ranking for improved retrieval quality

✅ **RAG Pipeline Implementation**
- Integrated LLaMA3-70B-8192 via Groq API with LangChain
- Created custom prompt templates for movie recommendations
- Successfully tested retrieval and generation pipeline

✅ **Initial Evaluation**
- Implemented Precision, Recall, and F1-score metrics
- Tested on sample queries with ground truth comparison
- Documented baseline performance metrics

### In Progress

🔄 **Performance Optimization**
- Fine-tuning retrieval parameters (currently k=500)
- Experimenting with different embedding models
- Optimizing query processing pipeline

🔄 **Evaluation Enhancement**
- Expanding test query dataset
- Comparing against baseline recommendation methods
- Conducting user study for explainability assessment

---

## Next Steps

### Short-term (1-2 weeks)

1. **Expand Evaluation**
   - Create comprehensive test set with 50+ diverse queries
   - Implement comparison with collaborative filtering baseline
   - Add qualitative analysis of explanations

2. **Improve Recall**
   - Experiment with hybrid retrieval (graph + vector search)
   - Implement query expansion techniques
   - Add constraint-based filtering before semantic retrieval

3. **Code Refactoring**
   - Create modular pipeline components
   - Add error handling and logging
   - Document all functions and classes

### Long-term (3-4 weeks)

4. **Web Interface Development**
   - Build Streamlit application for interactive demos
   - Add visualization of retrieved knowledge triplets
   - Implement session handling for multi-turn conversations

5. **Advanced Features**
   - Multi-hop reasoning over knowledge graph
   - Personalized recommendations based on user history
   - Integration of multiple LLMs for comparison

6. **Final Report & Presentation**
   - Comprehensive evaluation with statistical significance tests
   - Detailed analysis of strengths and limitations
   - Preparation of demo video and presentation slides

---

## Repository Structure

```
├── CMPE258_Project_Code.ipynb    # Main implementation notebook
├── CMPE258_ProjectProposal.pdf   # Project proposal document
├── README.md                      # Project documentation
└── pipeline.png                   # Architecture diagram
```

---

##  References

- [Lewis et al. (2021). Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)  
- [Hogan et al. (2022). Knowledge Graphs](https://doi.org/10.1145/3447772)  
- [KG-Retriever (2023)](https://arxiv.org/html/2412.05547v1)  
- [Nair & Cheriyan (2023)](https://doi.org/10.1109/idciot56793.2023.10053435)  
- [Xu et al. (2024)](https://doi.org/10.1145/3626772.3661370)  
- [Neo4j Example Datasets](https://neo4j.com/docs/getting-started/appendix/example-data/)

---