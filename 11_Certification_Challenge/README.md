# InsuranceLens 🔍

**AI-powered German Health Insurance Assistant**

InsuranceLens is an intelligent assistant that helps users understand their German health insurance policies through AI-powered analysis, highlighting unusual clauses, and providing personalized answers to insurance questions.

## 🎯 What it Does

- **Policy Analysis**: Upload your German health insurance PDF and get automatic analysis
- **Clause Highlighting**: Identifies 3-5 clauses that differ from industry standards
- **AI Q&A**: Ask specific questions about your policy or general insurance topics
- **Citation Support**: Get answers with precise citations from your documents
- **Web Search Integration**: General insurance questions answered via web search

## 🏗️ Architecture

- **Backend**: Python FastAPI with LangGraph orchestration
- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **AI**: OpenAI GPT models with LangChain
- **Vector DB**: Qdrant for semantic search
- **Web Search**: Tavily for general insurance questions

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- Tavily API key (for web search)

### Backend Setup

1. **Clone and navigate to backend**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # OR using uv (recommended)
   uv sync
   ```

3. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start Qdrant (Docker)**:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

5. **Run the backend**:
   ```bash
   # Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # OR using the main module
   python -m app.main
   ```

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Environment setup**:
   ```bash
   cp .env.local.example .env.local
   # Edit if you changed the backend URL
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

5. **Open in browser**:
   ```
   http://localhost:3000
   ```

## 📁 Project Structure

```
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── core/              # Configuration and settings
│   │   ├── models/            # Pydantic schemas
│   │   ├── api/               # API routes
│   │   ├── services/          # Business logic
│   │   └── agents/            # LangGraph agents
│   ├── tests/                 # Backend tests
│   └── pyproject.toml         # Dependencies
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/       # React components
│   │   ├── types/            # TypeScript definitions
│   │   └── utils/            # Utility functions
│   └── package.json          # Frontend dependencies
├── data/                     # Seed data and norms
│   └── norms_health_de_v1.json
└── README.md
```

## 🔧 Environment Variables

### Backend (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional
QDRANT_HOST=localhost
QDRANT_PORT=6333
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🎨 Features

### 📤 **File Upload**
- Drag & drop PDF upload
- Real-time progress tracking
- File validation and error handling

### 📊 **Policy Overview (Übersicht)**
- Basic policy information
- Quick access to common questions
- Upload statistics

### ⚠️ **Highlights**
- Automated clause analysis
- Comparison with industry norms
- Detailed explanations of unusual clauses

### ❓ **Questions (Fragen)**
- Natural language question interface
- AI-powered routing (policy vs. general questions)
- Citations for policy-specific answers
- Web sources for general questions

## 🤖 AI Components

- **Question Classification**: Routes questions to appropriate handlers
- **RAG Pipeline**: Retrieval-augmented generation for policy questions
- **Web Search**: Tavily integration for general insurance topics
- **Clause Analysis**: Comparison with German insurance norms database

## 🧪 Development

### Backend Development
```bash
cd backend

# Run tests
pytest

# Code formatting
black app/
isort app/

# Type checking
mypy app/
```

### Frontend Development
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build

# Lint
npm run lint
```

## 📚 API Documentation

When running in development mode, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔍 Key Endpoints

- `POST /api/v1/policies/upload` - Upload policy PDF
- `GET /api/v1/policies/{id}/overview` - Get policy overview
- `POST /api/v1/questions/ask` - Ask questions
- `GET /api/v1/health` - Health check

## 🚢 Deployment

### Backend (Railway/Render)
1. Connect your repository
2. Set environment variables
3. Deploy from `backend/` directory

### Frontend (Vercel)
1. Connect your repository
2. Set build directory to `frontend/`
3. Add environment variables
4. Deploy

## 🤝 Contributing

1. Create feature branch from `main`
2. Make your changes
3. Test thoroughly
4. Create pull request

## 📄 License

This project is created for educational purposes as part of the AI Makerspace bootcamp.

## 🔗 Links

- [AI Makerspace](https://aimakerspace.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

**Built with ❤️ for German health insurance clarity**
