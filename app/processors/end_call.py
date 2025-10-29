from pipecat.frames.frames import Frame, TextFrame, EndFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class EndCallProcessor(FrameProcessor):
    """Processor that allows bot to end the call by detecting specific phrases"""
    
    def __init__(self):
        super().__init__()
        self._end_phrases = [
            "goodbye", "bye", "end call", "hang up", 
            "that's all"
        ]
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        # Check if assistant said goodbye
        if isinstance(frame, TextFrame) and direction == FrameDirection.DOWNSTREAM:
            text_lower = frame.text.lower()
            for phrase in self._end_phrases:
                if phrase in text_lower:
                    print(f"Bot ending call, detected phrase: {phrase}")
                    # Push EndFrame to close connection
                    await self.push_frame(EndFrame())
                    break
        
        await self.push_frame(frame, direction)
