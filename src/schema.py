"""Collection of all request/response schemas."""
import enum
from typing import Any
from typing import List
from typing import Mapping
from typing import List, Union

from pydantic import BaseModel


class TTSRequest(BaseModel):
    """
    Request model for TTS API.
    Attributes:
        text (Union[List[str], str]): The text or list of texts to be converted to speech.
        filenames (Union[List[str], str]): The filenames of audio files to be saved on S3
        voice (str): The voice to use for the TTS conversion.
        temperature (float): Control audio emotional fluctuation, range is 0-1, the larger the number, the greater the fluctuation
        top_P (float): Control audio emotional relevance, range is 0.1-0.9, the larger the number, the higher the relevance
        top_K (float): Control audio emotional similarity, range is 1-20, the smaller the number, the higher the similarity
        manual_seed (int): Configure audio seed value, different seeds correspond to different tones
        bucket_name(str): S3 Bucket in which the audio file will be stored
        s3_path (str): Path of folder inside S3 bucket
    """

    text: Union[List[str], str]
    filenames: Union[List[str], str]
    voice: str = "Narration-3"
    temperature: float = 0.5
    top_P: float = 0.7
    top_K: float = 20
    manual_seed: int = None
    bucket_name: str = "immersfy-comic-scripts"
    s3_path: str

class AllocationRequest(BaseModel):
    character_list: dict