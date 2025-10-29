from fastapi import WebSocket

from app.services import run_bot


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for raw communication"""
    await websocket.accept()
    print("WebSocket connection successfuly established")
    
    try:
        await run_bot(websocket)
    except Exception as e:
        print(f"Error WebSocket: {e}")
    finally:
        print("WebSocket connection closed")
