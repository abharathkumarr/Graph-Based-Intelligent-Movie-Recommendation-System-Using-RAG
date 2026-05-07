# Changelog

All notable changes to the Graph-Based Movie Recommendation System project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-07

### Added
- Initial implementation of RAG-based movie recommendation system
- Neo4j knowledge graph integration with 28,865 nodes and 166,262 edges
- 229,894 knowledge triplets extracted and converted to natural language
- Sentence embedding generation using SentenceTransformers (all-MiniLM-L6-v2)
- FAISS index for efficient similarity search
- LangChain pipeline with Groq's llama-3.3-70b-versatile model
- Streamlit web application with interactive UI
- Natural language query interface
- Knowledge graph visualization as background
- Example queries with one-click execution
- Real-time response display with processing metrics
- Session state management for user queries
- Comprehensive project documentation (README, USAGE, MODEL_FILES)
- Architecture diagram showing complete RAG pipeline
- MIT License for open-source distribution
- Contributing guidelines and code style standards
- Deployment guide for local, cloud, and Docker setups
- Dependency management files (requirements.txt, requirements_ui.txt)

### Features
- **Query Processing**: Natural language movie queries with semantic understanding
- **Retrieval**: Top-500 triplet retrieval with cosine similarity reranking
- **Generation**: Context-aware recommendations using LLaMA 3.3 70B
- **UI/UX**: Clean blue/black/white theme matching knowledge graph aesthetics
- **Caching**: Automatic model caching for improved performance
- **Error Handling**: Graceful handling of API errors and missing files

### Performance
- Average Precision@10: 0.65
- Average Recall@10: 0.26
- Average F1-score@10: 0.30
- Average Response Time: 2-3 seconds
- Model Loading Time: ~30 seconds (first load, then cached)

### Documentation
- Comprehensive README with project overview
- Step-by-step usage guide with examples
- Deployment instructions for multiple platforms
- Contributing guidelines for developers
- Model file obtainment instructions
- Troubleshooting section for common issues

### Security
- Removed hardcoded API keys from codebase
- Environment variable-based configuration
- .gitignore to prevent secret commits
- GitHub push protection compliance

### Known Limitations
- Model files (346MB) not included in repository due to GitHub size limits
- Requires minimum 8GB RAM for running locally
- First load takes time due to large embedding file
- Groq API rate limits may affect high-volume usage

### System Requirements
- Python 3.8 or higher
- 8GB+ RAM recommended
- Groq API key required
- ~350MB storage for model files

### Supported Platforms
- macOS, Linux, Windows (local)
- Streamlit Cloud
- AWS EC2
- Google Colab
- Docker containers

## [Unreleased]

### Planned Features
- Multi-hop reasoning over knowledge graph
- Hybrid retrieval (vector + graph traversal)
- Query expansion and preprocessing
- User authentication and personalized recommendations
- Recommendation history and favorites
- Movie poster and trailer integration
- Export functionality (PDF, CSV)
- Mobile-responsive design improvements
- Alternative LLM support (GPT-4, Claude)
- Unit tests and integration tests
- Performance benchmarking suite
- A/B testing framework

### Under Consideration
- Real-time graph updates
- Collaborative filtering integration
- Multi-language support
- Voice query interface
- Movie rating predictions
- Watchlist management
- Social features (sharing, reviews)

## Version History

- **1.0.0** (2026-05-07) - Initial Release
  - Core RAG pipeline implementation
  - Streamlit web application
  - Complete documentation

---

## Commit Convention

We follow conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style/formatting
- `refactor:` Code restructuring
- `test:` Testing additions/updates
- `chore:` Maintenance tasks

## Contributors

- Bharath Kumar A (@abharathkumarr)
- Saripella Sriyavarma
- Venkata Siva Sai Krishna Prasad Y

## License

MIT License - See LICENSE file for details
