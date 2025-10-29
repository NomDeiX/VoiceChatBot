import asyncio
from fastapi import WebSocket, WebSocketDisconnect

from pipecat.frames.frames import AudioRawFrame, EndFrame, LLMMessagesFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_response import (
    LLMAssistantResponseAggregator,
    LLMUserResponseAggregator,
)
from pipecat.services.deepgram import DeepgramSTTService, DeepgramTTSService
from pipecat.services.openai import OpenAILLMService

from app.core.config import (
    DEEPGRAM_API_KEY,
    OPENAI_API_KEY,
    SAMPLE_RATE,
    CHANNELS,
    OPENAI_MODEL,
    DEEPGRAM_VOICE,
    DEEPGRAM_BASE_URL,
    SYSTEM_PROMPT,
)
from app.processors import AudioOutputProcessor, EndCallProcessor


async def run_bot(websocket: WebSocket):
    """Main bot logic with Pipecat pipeline"""
    
    # Get API keys
    deepgram_api_key = DEEPGRAM_API_KEY
    openai_api_key = OPENAI_API_KEY
    
    if not deepgram_api_key or not openai_api_key:
        print("Warning: API keys not set. Set DEEPGRAM_API_KEY and OPENAI_API_KEY environment variables")
    
    # Initialize services
    stt = DeepgramSTTService(
        api_key=deepgram_api_key,
        base_url=DEEPGRAM_BASE_URL,
        encoding="linear16",
        sample_rate=SAMPLE_RATE
    )
    
    llm = OpenAILLMService(
        api_key=openai_api_key,
        model=OPENAI_MODEL
    )
    
    tts = DeepgramTTSService(
        api_key=deepgram_api_key,
        voice=DEEPGRAM_VOICE,
        encoding="linear16",
        sample_rate=SAMPLE_RATE
    )
    

    params = PipelineParams(
        allow_interruptions=True,
        enable_metrics=False,
        send_initial_empty_metrics=False,
        enable_usage_metrics=False,
        observers=[] 
    )
    
    # User and assistant response aggregators
    user_aggregator = LLMUserResponseAggregator()
    assistant_aggregator = LLMAssistantResponseAggregator()
    
    # Audio output capturer
    audio_output = AudioOutputProcessor()
    
    # End call processor for bonus task
    end_call_processor = EndCallProcessor()
    
    # System prompt with end call instruction
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
    

    pipeline = Pipeline([
        stt,
        user_aggregator,
        llm,
        tts,
        assistant_aggregator,
        end_call_processor,
        audio_output, 
    ])
    
    task = PipelineTask(
        pipeline,
        params=params
    )
    
    # Initialize conversation
    await task.queue_frame(LLMMessagesFrame(messages))
    

    runner = PipelineRunner()
    pipeline_task = asyncio.create_task(runner.run(task))
    
    # Task to send audio to WebSocket
    async def send_audio_to_websocket():
        """Send audio from pipeline to WebSocket"""
        try:
            async for frame in audio_output.get_audio_frames():
                if isinstance(frame, AudioRawFrame):
                    await websocket.send_bytes(frame.audio)
                elif isinstance(frame, EndFrame):
                    print("End frame received, closing WebSocket")
                    break
        except Exception as e:
            print(f"Error sending audio: {e}")
        finally:
            try:
                await websocket.close()
            except:
                pass
    
    # Task to receive audio
    async def receive_audio_from_websocket():
        """Receive audio from WebSocket and push to pipeline"""
        frame_counter = 1000000  # Start with high number to avoid conflicts
        try:
            while True:
                data = await websocket.receive_bytes()
                
                audio_frame = AudioRawFrame(
                    audio=data,
                    sample_rate=SAMPLE_RATE,
                    num_channels=CHANNELS
                )
                # Manually set id to avoid observer attribute error
                audio_frame.id = frame_counter
                frame_counter += 1
                
                await task.queue_frame(audio_frame)
                
        except WebSocketDisconnect:
            print("WebSocket disconnected by client")
        except Exception as e:
            print(f"Error receiving audio: {e}")
        finally:
            await task.queue_frame(EndFrame())
    
    try:
        # Run both send and receive tasks concurrently
        await asyncio.gather(
            send_audio_to_websocket(),
            receive_audio_from_websocket(),
            pipeline_task,
            return_exceptions=True
        )
    except Exception as e:
        print(f"Error in bot: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            await websocket.close()
        except:
            pass
