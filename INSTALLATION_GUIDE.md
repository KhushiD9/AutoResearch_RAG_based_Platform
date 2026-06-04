# Complete Installation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Verification](#verification)
5. [Running the Application](#running-the-application)
6. [Common Issues](#common-issues)

## Prerequisites

### Required Software

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

3. **Git** (optional, for version control)
   - Download from: https://git-scm.com/

### Required API Keys

1. **Google Gemini API Key** (Required)
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

2. **OpenAI API Key** (Optional)
   - Visit: https://platform.openai.com/api-keys
   - Sign up or log in
   - Create new API key
   - Copy the key

## Backend Setup

### Step 1: Navigate to Backend Directory

```cmd
cd backend
```

### Step 2: Create Virtual Environment

Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web framework)
- PyPDF2 and pdfplumber (PDF processing)
- ChromaDB (vector database)
- Google Generative AI (Gemini)
- OpenAI (optional LLM)
- arXiv and other dependencies

Wait for installation to complete (2-5 minutes).

### Step 4: Create Configuration File

```cmd
copy .env.example .env
```

Or manually create `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 5: Edit Configuration

Open `.env` in a text editor and:
1. Replace `your_gemini_api_key_here` with your actual Gemini API key
2. (Optional) Replace `your_openai_api_key_here` with your OpenAI key
3. Save the file

### Step 6: Verify Setup

Run the verification script:
```cmd
python verify_setup.py
```

If all checks pass, you're ready to go!

## Frontend Setup

### Step 1: Navigate to Frontend Directory

Open a NEW terminal window (keep backend terminal open) and:

```cmd
cd frontend
```

### Step 2: Install Dependencies

```cmd
npm install
```

This will install:
- Angular framework and CLI
- TypeScript
- RxJS
- Development tools

Wait for installation to complete (3-10 minutes).

### Step 3: Verify Installation

Check if Angular CLI is available:
```cmd
npx ng version
```

You should see Angular CLI version information.

## Verification

### Backend Verification

In the backend terminal, start the server:
```cmd
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open browser to: http://localhost:8000/docs

You should see the interactive API documentation.

Press `Ctrl+C` to stop the server.

### Frontend Verification

In the frontend terminal, start the dev server:
```cmd
npm start
```

You should see:
```
** Angular Live Development Server is listening on localhost:4200
✔ Compiled successfully.
```

Open browser to: http://localhost:4200

You should see the Research Paper Assistant interface.

Press `Ctrl+C` to stop the server.

## Running the Application

### Start Backend

In terminal 1:
```cmd
cd backend
venv\Scripts\activate
python main.py
```

Keep this running.

### Start Frontend

In terminal 2:
```cmd
cd frontend
npm start
```

Keep this running.

### Access Application

Open browser to: http://localhost:4200

## Common Issues

### Backend Issues

#### Issue: "Module not found" error

**Solution:**
```cmd
pip install -r requirements.txt
```

#### Issue: "No module named 'venv'"

**Solution:**
Ensure virtual environment is activated:
```cmd
venv\Scripts\activate
```

#### Issue: "GEMINI_API_KEY not set"

**Solution:**
1. Check `.env` file exists
2. Verify API key is correctly pasted
3. No spaces around the `=` sign
4. No quotes around the key

#### Issue: "Port 8000 already in use"

**Solution:**
Find and kill the process using port 8000:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

#### Issue: "npm command not found"

**Solution:**
Install Node.js from https://nodejs.org/

#### Issue: "Cannot find module '@angular/core'"

**Solution:**
```cmd
rmdir /s node_modules
npm install
```

#### Issue: "Port 4200 already in use"

**Solution:**
```cmd
npx ng serve --port 4201
```

#### Issue: CORS errors in browser console

**Solution:**
1. Ensure backend is running on port 8000
2. Check CORS configuration in `backend/main.py`
3. Restart both servers

### API Issues

#### Issue: "Failed to search papers"

**Solution:**
1. Check internet connection
2. Verify API key is valid
3. Check API quota/limits
4. Try a different topic

#### Issue: "No PDF available"

**Solution:**
- Some papers don't have open-access PDFs
- Try different topics
- Semantic Scholar has more open-access papers than arXiv for some fields

#### Issue: "ChromaDB error"

**Solution:**
```cmd
rmdir /s chroma_db
```
Restart backend to recreate database.

## Testing the Application

### Test 1: Search Papers

1. Go to "Search Papers" page
2. Enter topic: "machine learning"
3. Select 3 papers
4. Click "Search Papers"
5. Wait 1-2 minutes
6. Should see results with processed papers

### Test 2: Ask Questions

1. Go to "Ask Questions" page
2. Select the collection you just created
3. Ask: "What are the main findings?"
4. Should receive an AI-generated answer with sources

### Test 3: View History

1. Go to "History" page
2. Should see your previous question
3. Try deleting an entry

## Next Steps

Once everything is working:

1. **Explore different topics**: Try various research areas
2. **Try query modes**: Test Compare, Review, and Gaps modes
3. **Check API docs**: Visit http://localhost:8000/docs
4. **Customize**: Modify colors, add features
5. **Deploy**: Consider deployment to cloud platforms

## Getting Help

If you encounter issues:

1. Check this guide's "Common Issues" section
2. Review error messages carefully
3. Ensure all prerequisites are installed
4. Verify API keys are correct
5. Check that both servers are running

## Success Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] `.env` file created with API keys
- [ ] Frontend dependencies installed
- [ ] Backend server starts without errors
- [ ] Frontend dev server starts without errors
- [ ] Can access http://localhost:4200
- [ ] API docs available at http://localhost:8000/docs
- [ ] Successfully searched for papers
- [ ] Successfully asked a question
- [ ] History page shows saved queries

## Deployment (Optional)

For production deployment:

1. Build frontend: `npm run build`
2. Deploy `dist/` folder to web server
3. Set up proper Python hosting (Gunicorn, etc.)
4. Configure environment variables securely
5. Set up HTTPS
6. Configure production database
7. Set up monitoring and logging

Congratulations! You now have a fully functional AI-powered research assistant.
