import streamlit as st
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import faiss
import time
import os
import base64

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_image(image_path):
    """Convert image to base64 for background"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def load_html_as_background():
    """Load knowledge graph HTML for background"""
    html_path = "knowledge_graph_ACTED_IN.html"
    if os.path.exists(html_path):
        return html_path
    return None

# Try to load knowledge graph HTML
kg_html_path = load_html_as_background()

# Check for knowledge graph image
bg_image_paths = [
    "assets/knowledge_graph_bg.png",
    "assets/image-3f8fe893-4bc2-487b-b0c3-1342ab56564b.png",
    "assets/image-b0ae0c14-ec03-4702-907d-12a9fc9803d7.png"
]

bg_image_b64 = None
for bg_path in bg_image_paths:
    if os.path.exists(bg_path):
        import base64
        with open(bg_path, "rb") as img_file:
            bg_image_b64 = base64.b64encode(img_file.read()).decode()
        break

if bg_image_b64:
    background_style = f"""
        background-image: linear-gradient(rgba(5, 10, 20, 0.50), rgba(10, 15, 25, 0.50)), 
                          url('data:image/png;base64,{bg_image_b64}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    """
else:
    # Fallback: CSS-based network visualization effect
    background_style = """
        background: 
            radial-gradient(circle at 20% 30%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 80% 20%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 40% 70%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 70% 60%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 30% 50%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 90% 80%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 15% 80%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            radial-gradient(circle at 60% 40%, rgba(100, 150, 255, 0.2) 0%, transparent 4%),
            rgba(5, 10, 20, 1);
        background-attachment: fixed;
    """

st.markdown(f"""
<style>
    /* Main background - semi-transparent to show graph */
    .stApp {{
        {background_style}
    }}
    
    /* Remove the pattern overlay to let graph show through */
    .stApp::before {{
        display: none;
    }}
    
    /* Title styling - Blue theme */
    .main-title {{
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #6ea8ff 0%, #4db8ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'Arial Black', sans-serif;
        animation: glow 2s ease-in-out infinite alternate;
        filter: drop-shadow(0 4px 8px rgba(110, 168, 255, 0.6));
    }}
    
    @keyframes glow {{
        from {{
            filter: drop-shadow(0 4px 8px rgba(110, 168, 255, 0.6));
        }}
        to {{
            filter: drop-shadow(0 6px 15px rgba(77, 184, 255, 0.8));
        }}
    }}
    
    .subtitle {{
        text-align: center;
        color: #ffffff;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
    }}
    
    /* Input box styling - Blue theme */
    .stTextInput > div > div > input {{
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
        border: 3px solid rgba(110, 168, 255, 0.6);
        border-radius: 15px;
        padding: 20px;
        font-size: 1.2rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        font-weight: 500;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #6ea8ff;
        box-shadow: 0 0 25px rgba(110, 168, 255, 0.8);
        background-color: rgba(0, 0, 0, 0.9);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
    }}
    
    /* Button styling - Blue theme for example queries */
    .stButton > button {{
        background: linear-gradient(135deg, #5b8fd9 0%, #6ea8ff 100%);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1.05rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(110, 168, 255, 0.3);
        width: 100%;
        text-align: left;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(110, 168, 255, 0.6);
        background: linear-gradient(135deg, #6ea8ff 0%, #4db8ff 100%);
        border-color: rgba(255, 255, 255, 0.6);
    }}
    
    /* Primary button (Get Recommendations) - Brighter Blue */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #4db8ff 0%, #6ea8ff 100%);
        border: 3px solid rgba(255, 255, 255, 0.6);
        padding: 18px 40px;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(77, 184, 255, 0.6);
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #6ea8ff 0%, #4db8ff 100%);
        box-shadow: 0 8px 30px rgba(77, 184, 255, 0.8);
    }}
    
    /* Result box styling - Blue background with white text */
    .result-box {{
        background: linear-gradient(135deg, #2d5f9e 0%, #3a7bc8 100%);
        border: 3px solid rgba(110, 168, 255, 0.8);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        backdrop-filter: blur(25px);
        box-shadow: 0 8px 32px rgba(110, 168, 255, 0.4);
    }}
    
    .result-title {{
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 15px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }}
    
    .result-content {{
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.9;
        white-space: pre-wrap;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        font-weight: 500;
    }}
    
    /* Example queries styling - Blue theme */
    .example-box {{
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid rgba(110, 168, 255, 0.4);
        border-radius: 12px;
        padding: 15px 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(15px);
    }}
    
    .example-box:hover {{
        background: rgba(110, 168, 255, 0.2);
        transform: translateX(5px);
        border-color: #6ea8ff;
        box-shadow: 0 4px 15px rgba(110, 168, 255, 0.4);
    }}
    
    .example-text {{
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }}
    
    /* Info boxes - IMPROVED */
    .info-box {{
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid rgba(72, 219, 251, 0.6);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        color: #48dbfb;
        backdrop-filter: blur(10px);
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }}
    
    .warning-box {{
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid rgba(255, 165, 0, 0.6);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        color: #ffa500;
        backdrop-filter: blur(10px);
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }}
    
    /* Expander styling - Blue theme */
    .streamlit-expanderHeader {{
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid rgba(110, 168, 255, 0.4);
        border-radius: 10px;
        color: #ffffff !important;
        font-weight: 600;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: rgba(110, 168, 255, 0.2);
        border-color: #6ea8ff;
    }}
    
    .streamlit-expanderContent {{
        background: rgba(0, 0, 0, 0.85);
        border: 2px solid rgba(110, 168, 255, 0.3);
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
    }}
    
    /* Hide Streamlit branding and empty elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Reduce spacing between elements */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 1rem;
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.05);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
    }}
    
    /* Spinner styling */
    .stSpinner > div {{
        border-top-color: #f093fb !important;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    """Load the RAG system components"""
    try:
        # Check if data files exist
        if not os.path.exists('triplet_sentences.pkl') or not os.path.exists('triplet_embeddings.pkl'):
            return None, None, None, "missing_files"
        
        # Load triplet sentences
        with open('triplet_sentences.pkl', 'rb') as f:
            triplet_sentences = pickle.load(f)
        
        # Load triplet embeddings
        with open('triplet_embeddings.pkl', 'rb') as f:
            triplet_embeddings = pickle.load(f)
        
        # Load embedding model
        encoder_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Build FAISS index
        dimension = triplet_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(triplet_embeddings).astype('float32'))
        
        # Create vectorstore
        index_to_docstore_id = {i: str(i) for i in range(len(triplet_sentences))}
        docstore = InMemoryDocstore({
            str(i): Document(page_content=triplet_sentences[i])
            for i in range(len(triplet_sentences))
        })
        
        vectorstore = FAISS(
            embedding_function=encoder_model.encode,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id
        )
        
        return vectorstore, encoder_model, triplet_sentences, "success"
    
    except Exception as e:
        return None, None, None, f"error: {str(e)}"

def create_qa_chain(vectorstore, groq_api_key):
    """Create the QA chain with Groq"""
    try:
        # Initialize LLM
        llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=groq_api_key
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 500})
        
        # Create prompt template
        prompt_template = PromptTemplate.from_template("""
You are a movie recommendation expert.

Use only the facts below. If the answer is not present, say you do not know.

Facts:
{context}

Question:
{question}

Answer:
""")
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt_template}
        )
        
        return qa_chain, None
    
    except Exception as e:
        return None, str(e)

def main():
    # Title and subtitle
    st.markdown('<h1 class="main-title">🎬 AI Movie Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Graph-Based Intelligent Movie Recommendation System Using RAG</p>', unsafe_allow_html=True)
    
    # Load RAG system
    vectorstore, encoder_model, triplet_sentences, status = load_rag_system()
    
    # Check API key
    groq_api_key = st.sidebar.text_input("🔑 Enter Groq API Key", type="password")
    
    if status == "missing_files":
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Model Data Not Found!</strong><br><br>
            Please follow these steps:<br>
            1. Run the code in <code>save_model_data.py</code> in your Colab notebook<br>
            2. Download <code>triplet_sentences.pkl</code> and <code>triplet_embeddings.pkl</code><br>
            3. Place them in the same folder as <code>app.py</code><br>
            4. Restart this Streamlit app
        </div>
        """, unsafe_allow_html=True)
        return
    
    elif status.startswith("error"):
        st.error(f"❌ Error loading model: {status}")
        return
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">🎯 Ask Me Anything About Movies!</h3>', unsafe_allow_html=True)
        
        # Query input - use session state for value
        if 'user_query' not in st.session_state:
            st.session_state.user_query = ""
        
        user_query = st.text_input(
            "",
            value=st.session_state.user_query,
            placeholder="e.g., Find action movies with Tom Hanks released after 2000...",
            label_visibility="collapsed",
            key="query_input"
        )
        
        # Submit button
        submit_button = st.button("🎬 Get Recommendations", type="primary", use_container_width=True)
        
        # Process query
        if submit_button and user_query:
            if not groq_api_key:
                st.warning("⚠️ Please enter your Groq API key in the sidebar!")
            else:
                with st.spinner('🎞️ Searching through 229,894 movie facts...'):
                    # Create QA chain
                    qa_chain, error = create_qa_chain(vectorstore, groq_api_key)
                    
                    if error:
                        st.error(f"❌ Error creating QA chain: {error}")
                    else:
                        try:
                            # Get response
                            start_time = time.time()
                            result = qa_chain.invoke({"query": user_query})
                            elapsed_time = time.time() - start_time
                            
                            # Display result
                            st.markdown("""
                            <div class="result-box">
                                <div class="result-title">🎯 AI Recommendations</div>
                                <div class="result-content">{}</div>
                                <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 15px;">⏱️ Response time: {:.2f}s</p>
                            </div>
                            """.format(result["result"], elapsed_time), unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Error processing query: {str(e)}")
        
        elif submit_button and not user_query:
            st.warning("⚠️ Please enter a query first!")
    
    with col2:
        st.markdown('<h3 style="color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">💡 Example Queries</h3>', unsafe_allow_html=True)
        
        example_queries = [
            ("🎬", "List adventure movies released after 2010"),
            ("⭐", "Find movies with rating above 8.0"),
            ("🎭", "Movies acted by Leonardo DiCaprio"),
            ("🎪", "Comedy movies produced in USA"),
            ("🎯", "Action movies with budget over $100M"),
            ("🌟", "Movies directed by Steven Spielberg"),
            ("🎨", "Recent movies in Adventure genre"),
            ("🎵", "Movies with Tom Hanks in Drama")
        ]
        
        for emoji, query in example_queries:
            if st.button(f"{emoji} {query}", key=f"ex_{query}", use_container_width=True):
                st.session_state.user_query = query
                st.rerun()
    
    # About section
    with st.expander("📖 About This Project", expanded=False):
        st.markdown("""
        <div style="color: #ffffff; font-size: 1.05rem; line-height: 1.8;">
        
        <h3 style="color: #6ea8ff;">Graph-Based Intelligent Movie Recommendation System</h3>
        
        <p><strong>Powered by:</strong></p>
        <ul>
        <li>🔷 <strong>Neo4j Knowledge Graph</strong> (28,865 nodes, 166,262 relationships)</li>
        <li>🧠 <strong>229,894 Knowledge Triplets</strong> extracted and converted to natural language</li>
        <li>🔍 <strong>FAISS Vector Search</strong> with 384-dimensional embeddings</li>
        <li>🤖 <strong>LLaMA3-70B</strong> via Groq API for intelligent recommendations</li>
        <li>⚡ <strong>RAG Architecture</strong> for fact-grounded, explainable results</li>
        </ul>
        
        <p><strong>Team: Group 19</strong></p>
        <ul>
        <li>Bharath Kumar A (018221268)</li>
        <li>Saripella Sriyavarma (019130553)</li>
        <li>Venkata Siva Sai Krishna Prasad Y (018320835)</li>
        </ul>
        
        <p><strong>Course:</strong> CMPE 258 - Deep Learning (Spring 2026)</p>
        
        <p><strong>GitHub:</strong> <a href="https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG" 
        style="color: #48dbfb;">View Repository</a></p>
        
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
