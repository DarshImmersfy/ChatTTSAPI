# main.py

import logging

from fastapi import FastAPI, HTTPException
import uvicorn

from chat_tts import ChatTTSWrapper
from src import schema, savedata, module


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize FastAPI app
app = FastAPI(title="Text-to-Speech API", description="A simple API to convert text to speech using the ChatTTSWrapper", version="1.0.0")

# Initialize the TTS wrapper
tts_wrapper = ChatTTSWrapper()


@app.post("/generate-audio/")
async def generate_audio(request: schema.TTSRequest):
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
        audio_files = tts_wrapper.generate_response(texts=request.text, voice=request.voice, temperature=request.temperature, top_P=request.top_P, top_K=request.top_K, manual_seed=request.manual_seed)

        if not audio_files:
            raise HTTPException(status_code=500, detail="Failed to generate audio")

        # Save the audio files on S3
        if isinstance(request.filenames, str):
            filenames = [request.filenames]
        else:
            filenames = request.filenames

        s3_links = []
        for filename, audio_file in zip(filenames, audio_files):
            s3_links.append({filename: savedata.upload_to_s3(request.bucket_name, audio_file, filename, request.s3_path, "audio/wav")})
            logging.info(f"Successfully uploaded: {filename} to S3")

        logging.info(f"Audio generated successfully for voice: {request.voice}")
        return {"s3_links": s3_links}

    except Exception as e:
        logging.error(f"Error occurred during audio generation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/allocate_voice/")
async def generate_audio(request: schema.AllocationRequest):
    try:
        character_dict = module.choose_voice(request)
        return character_dict
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
