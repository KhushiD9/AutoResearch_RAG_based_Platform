# 🚀 START HERE - Quick Guide

Welcome to the AI-Powered Research Paper Assistant! This guide will get you up and running in **10 minutes**.

## What This Application Does

Search for research papers → Process them with AI → Ask questions → Get intelligent answers with citations

---

## Prerequisites (5 minutes to install)

1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Google Gemini API Key** (FREE) - [Get it here](https://makersuite.google.com/app/apikey)

---

## Setup (5 minutes)

### Step 1: Backend Setup (3 minutes)

Open terminal/command prompt:

```cmd
cd backend
python -m venv venv
```

Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Install packages:
```cmd
pip install -r requirements.txt
```

Create config file:
```cmd
copy .env.example .env
```

Edit `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=paste_your_key_here
```

### Step 2: Frontend Setup (2 minutes)

Open a **NEW** terminal:

```cmd
cd frontend
npm install
```

---

## Run the Application

### Start Backend (Terminal 1)
```cmd
cd backend
venv\Scripts\activate
python main.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

### Start Frontend (Terminal 2)
```cmd
cd frontend
npm start
```

Wait for: `Compiled successfully`

### Open Browser
Go to: **http://localhost:4200**

---

## Try It Out (2 minutes)

### 1. Search for Papers
- Enter topic: **"machine learning"**
- Select: **3 papers**
- Click: **"Search Papers"**
- Wait: 1-2 minutes for processing

### 2. Ask Questions
- Go to: **"Ask Questions"** tab
- Select your collection
- Ask: **"What are the main findings?"**
- Get your answer with citations!

### 3. View History
- Go to: **"History"** tab
- See all your previous queries

---

## Troubleshooting

### Backend won't start?
- Check you added your API key to `.env`
- Make sure virtual environment is activated
- Check Python version: `python --version`

### Frontend won't start?
- Check Node.js is installed: `node --version`
- Try: `rmdir /s node_modules` then `npm install` again

### No papers found?
- Try a different topic
- Check your internet connection
- Some topics have limited open-access papers

### API key error?
- Make sure you copied it correctly
- No spaces or quotes around the key
- Get a new key if needed

---

## What to Do Next

1. ✅ **Try different topics**: "neural networks", "quantum computing", "climate change"
2. ✅ **Try different modes**: Compare, Literature Review, Research Gaps
3. ✅ **Read the docs**: Check out README.md for more features
4. ✅ **Customize**: Modify the UI colors and styles
5. ✅ **Deploy**: Use DEPLOYMENT.md to go live

---

## File Guide

- **README.md** - Full project documentation
- **QUICKSTART.md** - Detailed setup instructions
- **API_DOCUMENTATION.md** - API reference
- **FEATURES.md** - What the app can do
- **PROJECT_SUMMARY.md** - What was built

---

## Key Features

🔍 **Multi-Source Search** - Semantic Scholar + arXiv
📄 **Automatic PDF Processing** - Download and extract text
🤖 **AI-Powered Answers** - Using Gemini or OpenAI
📚 **Multiple Query Modes** - Q&A, Compare, Review, Gaps
✨ **Beautiful UI** - Modern glassmorphism design
📊 **Query History** - Track all your research

---

## Important URLs

- **Application**: http://localhost:4200
- **API Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api
- **Health Check**: http://localhost:8000/health

---

## Getting Help

1. Check the troubleshooting section above
2. Read the INSTALLATION_GUIDE.md
3. Review error messages carefully
4. Make sure both backend and frontend are running
5. Check browser console for errors (F12)

---

## Example Topics to Try

✅ **Computer Science**: "machine learning", "neural networks", "quantum computing"
✅ **Physics**: "black holes", "quantum mechanics", "string theory"
✅ **Medicine**: "cancer treatment", "immunotherapy", "gene therapy"
✅ **Engineering**: "renewable energy", "robotics", "nanotechnology"
✅ **Biology**: "CRISPR", "protein folding", "genetic algorithms"
✅ **Chemistry**: "catalysis", "organic synthesis", "materials science"

---

## Quick Commands Reference

### Backend
```cmd
# Start
cd backend
venv\Scripts\activate
python main.py

# Verify setup
python verify_setup.py

# Stop
Ctrl+C
```

### Frontend
```cmd
# Start
cd frontend
npm start

# Build for production
npm run build

# Stop
Ctrl+C
```

---

## Success Checklist

Before asking questions, make sure:

- [ ] Backend is running (check terminal output)
- [ ] Frontend is running (check terminal output)
- [ ] Browser shows the application at localhost:4200
- [ ] API docs load at localhost:8000/docs
- [ ] You've searched for and indexed papers
- [ ] You've selected a collection in the chat interface

---

## Tips for Best Results

1. **Start with popular topics** - They have more open-access papers
2. **Use 3-5 papers** - Good balance of speed and coverage
3. **Be specific with questions** - Better answers
4. **Try different modes** - Each mode has different strengths
5. **Keep terminals open** - Don't close the backend/frontend terminals

---

## Architecture at a Glance

```
User → Angular Frontend → FastAPI Backend → {
    Semantic Scholar API (search papers)
    arXiv API (search papers)
    PDF Download & Extract
    Gemini (embeddings & LLM)
    ChromaDB (vector storage)
} → Intelligent Answer
```

---

## What Makes This Special?

✨ **RAG Architecture** - Retrieval-Augmented Generation
✨ **Multiple Sources** - More papers, better answers
✨ **Citation-Backed** - All answers include sources
✨ **Modern Design** - Beautiful glassmorphism UI
✨ **Production Ready** - Deploy immediately
✨ **Well Documented** - Easy to understand and extend

---

## Support

If you're stuck:
1. Read the error message carefully
2. Check the troubleshooting section
3. Review the INSTALLATION_GUIDE.md
4. Make sure prerequisites are installed correctly
5. Verify API key is set correctly

---

## Congratulations!

You now have a fully functional AI-powered research assistant running on your machine. Start exploring the world of academic research with the power of AI!

**Happy Researching! 📚🤖**

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| Start Backend | `cd backend && venv\Scripts\activate && python main.py` |
| Start Frontend | `cd frontend && npm start` |
| View API Docs | http://localhost:8000/docs |
| Open App | http://localhost:4200 |
| Stop Servers | `Ctrl+C` in each terminal |

---

**Next Step**: Open http://localhost:4200 and start searching for papers!
