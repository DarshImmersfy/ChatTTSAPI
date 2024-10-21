---

# FastAPI Text-to-Speech (TTS) API

This repository hosts a FastAPI application that provides a Text-to-Speech (TTS) service using **Chat TTS model** for generating voice cues in comic scripts. The API uses a TTS model to convert text input into speech and uploads the generated audio files to an AWS S3 bucket.

## Features

- Generate speech from text using Chat TTS model.
- Save generated audio files to an AWS S3 bucket.
- Customizable voice settings, including voice type, temperature, emotional relevance, and tone similarity.
- Log generation and management via a systemd service.

## Requirements

- Python 3.10
- AWS credentials with permissions to upload to an S3 bucket.
- Dependencies specified in `requirements.txt`.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up AWS Credentials

Create a `.env` file in the root directory with the following content:

```plaintext
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

Replace the placeholders with your actual AWS credentials.

### 3. Run the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

The application will be accessible at `http://<your-ec2-ip>:8001`.

## Service Configuration

The application is managed by a systemd service named `narration.service` located at `/etc/systemd/system/narration.service`. Below is the configuration:

```plaintext
[Unit]
Description=FastAPI Narration Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/live/ChatTTSAPI
ExecStart=/home/ubuntu/live/ChatTTSAPI/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=3

# Logging
StandardOutput=file:/var/log/narration.log
StandardError=file:/var/log/narration.log

[Install]
WantedBy=multi-user.target
```

To manage the service, use the following commands:

- **Start the service**: `sudo systemctl start narration.service`
- **Stop the service**: `sudo systemctl stop narration.service`
- **Restart the service**: `sudo systemctl restart narration.service`
- **Enable the service on boot**: `sudo systemctl enable narration.service`

## API Endpoints

### 1. Root Endpoint

**Endpoint:** `/`  
**Method:** `GET`  
**Response:**  
Returns a message confirming the API is running.

### 2. Generate Audio and upload on S3

**Endpoint:** `/generate-audio/`  
**Method:** `POST`  
**Request Body:**  
```json
{
    "text": [
        "text-1",
        "text-2"
    ],
    "filenames": [
        "file-1.wav",
        "file-2.wav"
    ],
    "voice": "Female-1",
    "bucket_name": "immersfy-comic-scripts",
    "s3_path": "your_folder",
    "temperature": 0.5,
    "top_P": 0.7,
    "top_K": 20,
    "manual_seed": 12345,
}
```
Keys `temperature`, `top_P`, `top_K`, `manual_seed` are optional.

**Response:**  
Returns the S3 links of the uploaded audio files.
```json
{
    "s3_links": [
        {
            "file-1.wav": "s3://immersfy-comic-scripts//your_folder//file-1.wav"
        },
        {
            "file-2.wav": "s3://immersfy-comic-scripts//your_folder//file-2.wav"
        }
    ]
}
```

## Logging

Logs for the narration service are stored in `/var/log/narration.log`.

## Deployment on EC2

The application is hosted on an EC2 instance named **WebUI Instance** and runs on port **8001**.

---
