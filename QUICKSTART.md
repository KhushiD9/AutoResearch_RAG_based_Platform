# Quick Start Guide

## 1. Backend Setup (5 minutes)

Open a terminal and run:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```cmd
copy .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

Get a free API key from: https://makersuite.google.com/app/apikey

Start the backend:
```cmd
python main.py
```

## 2. Frontend Setup (3 minutes)

Open a NEW terminal and run:

```cmd
cd frontend
npm install
npm start
```

## 3. Use the Application

Open your browser to: http://localhost:4200

### Try it out:

1. **Search Papers**
   - Enter topic: "machine learning"
   - Click "Search Papers"
   - Wait for processing (1-2 minutes)

2. **Ask Questions**
   - Go to "Ask Questions" tab
   - Select your collection
   - Ask: "What are the main findings?"

3. **View History**
   - Check the "History" tab to see saved queries

## That's it!

You now have a fully functional AI-powered research assistant running locally.

## Troubleshooting

**Backend won't start?**
- Make sure you added your Gemini API key to `.env`
- Check if port 8000 is available

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

**No papers found?**
- Try a different topic
- Check your internet connection
- Some topics may have limited open-access papers

**Questions not working?**
- Make sure you indexed papers first in the Search tab
- Select a collection from the sidebar
- Backend must be running

## Next Steps

- Try different query modes (Compare, Review, Gaps)
- Experiment with different research topics
- Explore the API documentation at http://localhost:8000/docs
