from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.models import ChatMessage, AnalysisResult, HealthResponse
from app.vector_store import vector_store
from app.rag_chain import rag_chain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: Initialize vector store
    logger.info("Initializing vector store...")
    try:
        vector_store.initialize()
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="FIA Manipulation Pattern Analysis API",
    description="AI-powered API for analyzing relationship manipulation patterns using RAG",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(
        status="ok",
        message="FIA Manipulation Pattern Analysis API is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if vector store is initialized
        if vector_store.vector_store is None:
            raise HTTPException(status_code=503, detail="Vector store not initialized")

        return HealthResponse(
            status="healthy",
            message="All systems operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_story(message: ChatMessage):
    """
    Analyze a user's relationship story for manipulation patterns.

    This endpoint uses RAG to:
    1. Retrieve relevant manipulation patterns from the vector database
    2. Generate a contextual analysis using GPT-4
    3. Return structured findings with severity levels
    """
    try:
        logger.info(f"Analyzing message: {message.content[:100]}...")

        # Get analysis from RAG chain
        result = rag_chain.get_analysis(message.content)

        logger.info(f"Analysis complete. Patterns detected: {result.patterns_detected}")
        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze story: {str(e)}"
        )


@app.get("/patterns")
async def list_patterns():
    """
    List all manipulation patterns in the database.
    Useful for debugging and testing.
    """
    try:
        # Do a broad search to get samples
        docs = vector_store.similarity_search("manipulation pattern", k=20)
        patterns = list(set([doc.metadata.get('player_type', 'Unknown') for doc in docs]))
        return {
            "count": len(patterns),
            "patterns": patterns
        }
    except Exception as e:
        logger.error(f"Failed to list patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
