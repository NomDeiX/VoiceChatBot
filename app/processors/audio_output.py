import asyncio
from typing import AsyncGenerator

from pipecat.frames.frames import Frame, AudioRawFrame, EndFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class AudioOutputProcessor(FrameProcessor):
    """Processor that captures audio output frames"""
    
    def __init__(self):
        super().__init__()
        self._audio_queue = asyncio.Queue()
        
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        # Capture audio frames going downstream (to output)
        if isinstance(frame, AudioRawFrame) and direction == FrameDirection.DOWNSTREAM:
            await self._audio_queue.put(frame)
        
        # Also capture end frames
        if isinstance(frame, EndFrame):
            await self._audio_queue.put(frame)
            
        await self.push_frame(frame, direction)
    
    async def get_audio_frames(self) -> AsyncGenerator[Frame, None]:
        """Get audio frames as they're produced"""
        while True:
            frame = await self._audio_queue.get()
            yield frame
            if isinstance(frame, EndFrame):
                break
