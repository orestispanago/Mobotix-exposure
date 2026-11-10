import os

from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
load_dotenv(os.path.join(dirname, ".env"))

UPLOAD_PROTOCOL = os.getenv("UPLOAD_PROTOCOL", "ftp")
REMOTE_DIR = os.getenv("REMOTE_DIR")
FTP_IP = os.getenv("FTP_IP")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")
SFTP_KNOWN_HOSTS = os.path.join(dirname, "known_hosts")
CAM_IP = os.getenv("CAM_IP")
CAM_USER = os.getenv("CAM_USER")
CAM_PASS = os.getenv("CAM_PASS")
