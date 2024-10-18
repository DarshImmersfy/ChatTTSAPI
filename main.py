# main.py
from typing import List, Union
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import savedata
from chat_tts import ChatTTSWrapper

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize FastAPI app
app = FastAPI(title="Text-to-Speech API", description="A simple API to convert text to speech using the ChatTTSWrapper", version="1.0.0")

# Initialize the TTS wrapper
tts_wrapper = ChatTTSWrapper()


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


@app.post("/generate-audio/")
async def generate_audio(request: TTSRequest):
    """
    Endpoint to generate audio from text.
    Args:
        request (TTSRequest): The TTS request containing the text, voice and s3 parameters.
    Returns:
        dict: Contains the s3 links of audio data.
    Raises:
        HTTPException: If an error occurs during the TTS process.
    """
    try:
        logging.info(f"Generating audio for voice: {request.voice}")
        # Generate audio using the TTS wrapper
        audio_files = tts_wrapper.generate_response(text=request.text, voice=request.voice, temperature=request.temperature, top_P=request.top_P, top_K=request.top_K, manual_seed=request.manual_seed)

        if not audio_files:
            raise HTTPException(status_code=500, detail="Failed to generate audio")

        # Save the audio files on S3
        if isinstance(request.filenames, str):
            filenames = [request.filenames]
        else:
            filenames = request.filenames

        s3_links = []
        for filename, audio_file in zip(filenames, audio_files):
            s3_links.append(savedata.upload_to_s3(request.bucket_name, audio_file, filename, request.s3_path, "audio/wav"))

        logging.info(f"Audio generated successfully for voice: {request.voice}")
        return {"s3_links": s3_links}

    except Exception as e:
        logging.error(f"Error occurred during audio generation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def root():
    """
    Root endpoint to check the status of the API.
    Returns:
        dict: Simple message confirming the API is running.
    """
    return {"message": "Welcome to the Text-to-Speech API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
