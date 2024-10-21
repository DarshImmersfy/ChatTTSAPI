import io
import json
import logging
import boto3
from dotenv import load_dotenv

load_dotenv()

# Initialize S3 client
s3_client = boto3.client('s3')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_s3(bucket_name: str, content: str, file_name: str, s3_path: str, content_type: str) -> str:
    """
    Uploads content to an S3 bucket and returns the S3 file link.
    
    Parameters:
    bucket_name (str): The name of the S3 bucket.
    content (str): The content to be uploaded.
    file_name (str): The name of the file to be saved in the bucket.
    s3_path (str): The path within the S3 bucket where the file will be stored.
    content_type (str): The MIME type of the content (e.g., 'text/plain', 'application/json').
    
    Returns:
    str: The S3 URL of the uploaded file.
    
    Raises:
    Exception: If the upload fails, an exception is raised.
    """
    try:
        # Upload content to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{s3_path}/{file_name}",
            Body=content,
            ContentType=content_type
        )

        # Return the S3 link
        s3_url = f"s3://{bucket_name}/{s3_path}/{file_name}"
        return s3_url

    except Exception as e:
        # Log any exception that occurs during the upload
        logging.error(f"Failed to upload file '{file_name}' to S3: {str(e)}")
        raise e