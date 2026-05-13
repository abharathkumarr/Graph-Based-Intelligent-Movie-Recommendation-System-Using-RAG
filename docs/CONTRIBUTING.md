# Contributing to Graph-Based Movie Recommendation System

Thank you for your interest in contributing to our project! This guide will help you get started.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git installed on your machine
- Groq API key ([Get one here](https://console.groq.com))
- Basic knowledge of Python, LangChain, and knowledge graphs

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG.git
   cd Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG
   ```

2. **Install Dependencies**
   ```bash
   # For Jupyter notebook development
   pip install -r requirements.txt
   
   # For UI development
   pip install -r requirements_ui.txt
   ```

3. **Set Environment Variables**
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

4. **Get Model Files**
   - Follow instructions in `MODEL_FILES.md` to obtain required `.pkl` files
   - Place them in the project root directory

## How to Contribute

### Reporting Issues

Before creating an issue, please:
- Check if the issue already exists
- Provide clear description and steps to reproduce
- Include error messages, screenshots, or logs if applicable

### Suggesting Enhancements

We welcome enhancement suggestions! Please:
- Explain the use case and benefits
- Provide examples or mockups if possible
- Discuss potential implementation approaches

### Code Contributions

#### Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style and conventions
   - Add comments for complex logic
   - Update documentation as needed

3. **Test Your Changes**
   - Test the Streamlit UI: `streamlit run app_full.py`
   - Verify notebook cells run without errors
   - Check that no API keys are hardcoded

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```
   
   Follow conventional commit format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc.)
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Open a pull request on GitHub
   - Provide clear description of changes
   - Reference any related issues

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings to functions and classes

### Jupyter Notebooks
- Clear markdown cells explaining each section
- Remove output before committing (to reduce file size)
- No hardcoded API keys or credentials

### Streamlit UI
- Maintain consistent styling with existing theme
- Use caching (`@st.cache_resource`) for expensive operations
- Provide user feedback for loading states

## Areas for Contribution

### High Priority
- **Improve Recall**: Experiment with hybrid retrieval methods
- **Query Expansion**: Add query preprocessing and expansion
- **Multi-hop Reasoning**: Implement graph traversal for complex queries
- **Testing**: Add unit tests and integration tests

### Medium Priority
- **UI Enhancements**: Add more visualizations, filters, export options
- **Performance**: Optimize embedding loading and query processing
- **Documentation**: Add more examples, tutorials, video demos

### Low Priority
- **Alternative LLMs**: Support for other models (GPT-4, Claude, etc.)
- **Personalization**: User profiles and recommendation history
- **Deployment**: Docker containerization, cloud deployment guides

## Questions or Help?

Feel free to reach out to the team:
- **Bharath Kumar A**: bharathkumar.a@sjsu.edu
- **Saripella Sriyavarma**: sriyavarma.saripella@sjsu.edu
- **Venkata Siva Sai Krishna Prasad Y**: venkatasivasaikrishnaprasad.yedupati@sjsu.edu

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
