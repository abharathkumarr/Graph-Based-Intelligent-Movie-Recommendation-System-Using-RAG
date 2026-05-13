# Deployment Guide

This guide covers different deployment options for the Graph-Based Movie Recommendation System.

## Local Deployment

### Option 1: Quick Start (Recommended for Demo)

```bash
# Clone repository
git clone https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG.git
cd Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG

# Install dependencies
pip install -r requirements_ui.txt

# Obtain model files (see MODEL_FILES.md)
# Place triplet_sentences.pkl and triplet_embeddings.pkl in root directory

# Set API key
export GROQ_API_KEY="your_groq_api_key"

# Run application
./run_app.sh
```

Access at: `http://localhost:8502`

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_ui.txt

# Set environment variables
export GROQ_API_KEY="your_key"

# Launch Streamlit
streamlit run app_full.py --server.port 8502
```

## Cloud Deployment

### Streamlit Cloud (Easiest)

1. **Prerequisites**
   - GitHub repository with your code
   - Streamlit Cloud account (free)
   - Groq API key

2. **Setup Model Files**
   
   Since model files exceed 100MB, use one of these approaches:
   
   **Option A: External Storage**
   ```python
   # In app_full.py, add download logic
   import urllib.request
   
   def download_model_files():
       if not os.path.exists('triplet_embeddings.pkl'):
           url = "YOUR_CLOUD_STORAGE_URL/triplet_embeddings.pkl"
           urllib.request.urlretrieve(url, 'triplet_embeddings.pkl')
   ```
   
   Host files on:
   - Google Drive (with public link)
   - AWS S3
   - Dropbox
   - Hugging Face Hub

   **Option B: Generate on First Run**
   ```python
   # Add logic to generate embeddings on deployment
   # (Requires Neo4j credentials as secrets)
   ```

3. **Deploy to Streamlit Cloud**
   
   ```
   1. Go to https://streamlit.io/cloud
   2. Click "New app"
   3. Connect your GitHub repository
   4. Set main file: app_full.py
   5. Add secrets (Settings → Secrets):
      GROQ_API_KEY = "your_key"
   6. Deploy!
   ```

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   # Copy requirements
   COPY requirements_ui.txt .
   RUN pip install --no-cache-dir -r requirements_ui.txt
   
   # Copy application
   COPY app_full.py .
   COPY assets/ ./assets/
   
   # Model files should be volume-mounted
   VOLUME /app/models
   
   # Expose port
   EXPOSE 8502
   
   # Set environment
   ENV GROQ_API_KEY=""
   
   # Run app
   CMD ["streamlit", "run", "app_full.py", "--server.port=8502", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   # Build image
   docker build -t movie-rag-system .
   
   # Run container
   docker run -p 8502:8502 \
     -v $(pwd)/models:/app/models \
     -e GROQ_API_KEY="your_key" \
     movie-rag-system
   ```

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.large (8GB RAM minimum for model files)
   - Open port 8502 in security group

2. **Setup on EC2**
   ```bash
   # Connect to instance
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip python3-venv -y
   
   # Clone repository
   git clone https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG.git
   cd Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG
   
   # Setup environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements_ui.txt
   
   # Upload model files (use scp or aws s3 cp)
   # scp -i your-key.pem *.pkl ubuntu@your-ec2-ip:~/path/
   
   # Set API key
   echo "export GROQ_API_KEY='your_key'" >> ~/.bashrc
   source ~/.bashrc
   
   # Run with nohup
   nohup streamlit run app_full.py --server.port 8502 --server.address 0.0.0.0 &
   ```

3. **Access Application**
   - URL: `http://your-ec2-ip:8502`

### Google Colab (Temporary Demo)

```python
# In a Colab notebook
!git clone https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG.git
%cd Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG

!pip install -r requirements_ui.txt

# Upload model files or generate them
# Upload your API key
from google.colab import userdata
import os
os.environ['GROQ_API_KEY'] = userdata.get('GROQ_API_KEY')

# Run Streamlit with ngrok
!streamlit run app_full.py & npx localtunnel --port 8502
```

## Production Considerations

### Performance
- **Memory**: Minimum 8GB RAM for embedding files
- **CPU**: Multi-core recommended for concurrent users
- **Caching**: Streamlit caches loaded models automatically
- **Concurrency**: Consider load balancer for multiple users

### Security
- Never commit API keys to repository
- Use environment variables or secrets management
- Enable HTTPS for production deployment
- Implement rate limiting for API calls
- Validate user inputs to prevent injection attacks

### Monitoring
- Track API usage and costs (Groq API)
- Monitor response times and errors
- Log user queries (with privacy considerations)
- Set up alerts for system failures

### Scaling
- Use Redis for distributed caching
- Implement queue system for heavy queries
- Consider serverless functions for API calls
- Use CDN for static assets

## Troubleshooting

### Issue: Out of Memory
**Solution**: Upgrade to instance with more RAM or use streaming/chunking for embeddings

### Issue: Slow Loading
**Solution**: Pre-warm cache, optimize model loading, use SSD storage

### Issue: API Rate Limits
**Solution**: Implement exponential backoff, queue system, or upgrade API plan

### Issue: Port Already in Use
**Solution**: 
```bash
# Kill process on port 8502
lsof -ti:8502 | xargs kill -9

# Or use different port
streamlit run app_full.py --server.port 8503
```

## Cost Estimates

### Streamlit Cloud
- Free tier: Sufficient for demo/development
- Team tier: $200/month for more resources

### AWS EC2
- t2.large (8GB RAM): ~$70/month
- t2.xlarge (16GB RAM): ~$135/month
- Plus egress costs for data transfer

### Groq API
- Pay-as-you-go: Check current pricing at console.groq.com
- Estimate: ~$0.001-0.01 per query depending on context size

## Support

For deployment issues, contact:
- bharathkumar.a@sjsu.edu
- sriyavarma.saripella@sjsu.edu
- venkatasivasaikrishnaprasad.yedupati@sjsu.edu
