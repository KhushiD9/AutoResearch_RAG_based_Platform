from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import paper_routes, chat_routes, history_routes
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

app = FastAPI(
    title="Research Paper Assistant API",
    description="AI-powered research paper discovery and analysis — backed by Anthropic Claude + ChromaDB RAG",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paper_routes.router, prefix="/api/papers",  tags=["Papers"])
app.include_router(chat_routes.router,  prefix="/api/chat",    tags=["Chat"])
app.include_router(history_routes.router, prefix="/api/history", tags=["History"])

@app.get("/")
async def root():
    return {"message": "Research Paper Assistant API", "status": "running", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
