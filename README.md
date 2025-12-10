# 🔬 AI Research Agent - Phase 1 (Production Ready)

An intelligent research assistant that automatically searches, downloads, analyzes, and extracts insights from academic papers using LLM technology.

## Phase 1 Features

### **Stability & Reliability**
- Comprehensive error handling for all operations
- Graceful failure recovery (no crashes on broken PDFs or network issues)
- Detailed logging for debugging and monitoring
- Input validation and data cleaning

###  **Performance & Speed**
- **Smart caching system** (topic-based + paper-based)
- Results cached for 7 days (configurable)
- 80%+ reduction in API calls for repeated searches
- Instant results for cached queries

###  **AI-Powered Analysis**
- **LLM-based summaries** using Groq (free & fast)
- **3 detail levels**: Short, Medium (default), Long
- **Advanced research gap detection**:
  - Methodology gaps
  - Knowledge gaps
  - Future research directions
- **Key findings extraction**
- **Multiple citation formats** (APA, MLA, IEEE coming)

###  **Professional UI**
- Clean, modern interface
- Advanced filters (year range, open access)
- Sortable results (by relevance, year, citations)
- Tabbed paper views (Summary, Gaps, Findings, Citation, Status)
- Cache management dashboard
- Progress indicators

---

##  Quick Start

### 1. **Clone and Setup**

```bash
git clone <your-repo>
cd research-agent-v2

# Install dependencies
pip install -r requirements.txt
```

### 2. **Get API Keys**

#### Groq API (REQUIRED - FREE)
1. Go to https://console.groq.com/keys
2. Sign up (takes 30 seconds)
3. Create an API key
4. Copy the key

#### Semantic Scholar API (OPTIONAL)
1. Go to https://www.semanticscholar.org/product/api
2. Request an API key (increases rate limits)

### 3. **Configure Environment**

```bash
# Copy template
cp .env.template .env

# Edit .env and add your keys
nano .env  # or use any text editor
```

Your `.env` should look like:
```bash
GROQ_API_KEY=gsk_your_actual_key_here
SEMANTIC_SCHOLAR_API_KEY=  # optional
```

### 4. **Run Locally**

```bash
streamlit run app.py
```

Open browser at: `http://localhost:8501`

---

##  Project Structure

```
research-agent-v2/
├── agents/
│   ├── search_agent.py       # Semantic Scholar API with error handling
│   ├── pdf_agent.py          # Robust PDF download & extraction
│   ├── llm_agent.py          # Groq LLM integration
│   └── cache_manager.py      # Smart caching system
├── utils/
│   └── error_handler.py      # Error handling & logging
├── config.py                 # Configuration settings
├── research_agent.py         # Main orchestrator
├── app.py                    # Streamlit UI
├── requirements.txt
├── .env.template
├── .env                      # Your actual keys (DO NOT COMMIT)
└── README.md
```

---

##  Usage Guide

### **Basic Search**
1. Enter a research topic (e.g., "machine learning for drug discovery")
2. Click "Search Papers"
3. View AI-generated summaries and insights

### **Advanced Options (Sidebar)**

**Search Settings:**
- Adjust number of papers (1-50)
- Choose summary detail level
- Enable/disable PDF processing

**Filters:**
- Year range (e.g., 2020-2024)
- Open access only

**Cache Management:**
- View cache statistics
- Clear expired cache
- Clear all cache

### **Result Features**

Each paper card includes:
- **Summary Tab**: Abstract + full paper summaries
- **Research Gaps Tab**: Methodology, knowledge, and future directions
- **Key Findings Tab**: Main contributions and results
- **Citation Tab**: APA citation with copy button
- **Status Tab**: Processing status for each operation

---

##  Configuration

Edit `config.py` to customize:

```python
# Cache duration
CACHE_EXPIRY_DAYS = 7

# Default search limit
DEFAULT_PAPER_LIMIT = 10

# LLM model
GROQ_MODEL = "llama-3.1-70b-versatile"

# Summary levels
SUMMARY_LEVELS = {
    "short": {"max_tokens": 150},
    "medium": {"max_tokens": 300},
    "long": {"max_tokens": 600}
}
```

---

## 🌐 Deployment on Render

### **Option 1: Auto Deploy (Recommended)**

1. Push code to GitHub
2. Go to https://render.com
3. Create new "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add environment variable:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
7. Deploy!

### **Option 2: Manual Deploy**

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Create render.yaml
cat > render.yaml << EOF
services:
  - type: web
    name: research-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0
    envVars:
      - key: GROQ_API_KEY
        sync: false
EOF

# Deploy
render deploy
```

---

## Performance Metrics

### **Without Caching**
- Search + analyze 10 papers: ~60-90 seconds
- Repeated search: ~60-90 seconds (same time)

### **With Caching (Phase 1)**
- First search: ~60-90 seconds
- Repeated search: **< 2 seconds** 
- Cache hit rate: 80%+

### **PDF Processing**
- Average PDF download: 2-5 seconds
- Text extraction: 1-3 seconds per paper
- LLM analysis: 3-8 seconds per paper

---

##  Troubleshooting

### **"Groq API key not found"**
- Make sure `.env` file exists
- Check `GROQ_API_KEY` is set correctly
- Restart the app

### **"PDF processing failed"**
- Some PDFs are scanned images (no text)
- Some PDFs are password-protected
- Check logs in `research_agent.log`

### **"No papers found"**
- Try different keywords
- Remove year filters
- Check internet connection

### **Cache issues**
- Click "Clear All" in sidebar
- Delete `.cache` folder manually
- Restart app

---

## Logging

All operations are logged to:
- **Console**: Real-time logs
- **File**: `research_agent.log`

Log levels:
- `INFO`: Normal operations
- `WARNING`: Non-critical issues (cached used, PDF skipped)
- `ERROR`: Failures that don't crash the app
- `DEBUG`: Detailed debugging info

To change log level, edit `config.py`:
```python
LOG_LEVEL = "DEBUG"  # or INFO, WARNING, ERROR
```

---

##  What's Next? (Phase 2+)

Coming soon:
- Multiple data sources (ArXiv, PubMed, IEEE)
- Export to Word/PDF
- Literature review generator
- Multi-agent architecture
- Citation network visualization
- Collaborative features

---

##  Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

##  License

MIT License - feel free to use for personal or commercial projects

---

## Support

- **Issues**: Open a GitHub issue
- **Questions**: Start a discussion
- **Email**: your-email@example.com

---

##  Acknowledgments

- **Groq**: For free, fast LLM API
- **Semantic Scholar**: For excellent academic search API
- **Streamlit**: For easy Python web apps

---

**Built with ❤️ for researchers everywhere**
