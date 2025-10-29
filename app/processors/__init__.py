"""
Custom frame processors for the pipeline
"""

from .audio_output import AudioOutputProcessor
from .end_call import EndCallProcessor

__all__ = ["AudioOutputProcessor", "EndCallProcessor"]
