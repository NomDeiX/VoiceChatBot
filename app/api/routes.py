from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from .websocket import websocket_endpoint

# Initialize FastAPI app
app = FastAPI(
    title="Pipecat Voice Bot",
    description="Real-time voice assistant using Pipecat, FastAPI, and WebSockets",
    version="1.0.0"
)

# Register WebSocket endpoint
app.add_api_websocket_route("/ws", websocket_endpoint)


@app.get("/", response_class=HTMLResponse)
async def get():
    """Serve the frontend HTML"""
    html_path = Path(__file__).parent.parent / "templates" / "index.html"
    
    try:
        with open(html_path, "r") as f:
            html_content = f.read()
        return HTMLResponse(html_content)
    except FileNotFoundError:
        return HTMLResponse(
            "<h1>Error: index.html not found</h1>",
            status_code=500
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "voice-chatbot"}
