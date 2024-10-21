import os
from dotenv import load_dotenv

load_dotenv()
os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("AWS_SECRET_ACCESS_KEY")

MALE_VOICE_LIST = os.listdir(os.path.join("voices","embed","Male"))
FEMALE_VOICE_LIST = os.listdir(os.path.join("voices","embed","Female"))
NARRATION_VOICE_LIST = os.listdir(os.path.join("voices","embed","Narration"))