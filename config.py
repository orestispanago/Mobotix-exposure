import os

from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
load_dotenv(os.path.join(dirname, ".env"))

FTP_IP = os.getenv("FTP_IP")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
CAM_IP = os.getenv("CAM_IP")
CAM_USER = os.getenv("CAM_USER")
CAM_PASS = os.getenv("CAM_PASS")
