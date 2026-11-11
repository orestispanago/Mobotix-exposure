import datetime
import glob
import logging
import logging.config
import os
import time
import traceback

import ftp
import sftp
from camera import CamClient, exp_api_dict, exposure_times
from config import (
    CAM_IP,
    CAM_PASS,
    CAM_USER,
    FTP_IP,
    FTP_PASS,
    FTP_USER,
    REMOTE_DIR,
    SFTP_HOST,
    SFTP_KNOWN_HOSTS,
    SFTP_PASS,
    SFTP_PORT,
    SFTP_USER,
    UPLOAD_PROTOCOL,
)

dname = os.path.dirname(__file__)
os.chdir(dname)

os.makedirs("logs", exist_ok=True)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

LUX_MIN = 5000


def upload_files(local_files):
    if UPLOAD_PROTOCOL == "sftp":
        uploaded = sftp.upload_files(
            SFTP_HOST,
            SFTP_PORT,
            SFTP_USER,
            SFTP_PASS,
            SFTP_KNOWN_HOSTS,
            REMOTE_DIR,
            local_files,
        )
    else:
        uploaded = ftp.upload_files(
            FTP_IP, FTP_USER, FTP_PASS, REMOTE_DIR, local_files
        )
    return uploaded


def delete_local_files(local_files):
    for local_file in local_files:
        os.remove(local_file)
    logger.info(f"Deleted {len(local_files)} local files")


def delete_empty_dirs(local_files):
    for local_file in local_files:
        try:
            os.removedirs(os.path.dirname(local_file))
        except OSError:
            pass


def main():
    logger.info(f"{'-' * 15} START {'-' * 15}")

    now = datetime.datetime.now(datetime.timezone.utc)
    folder_name = now.strftime("%Y/%m/%d/%H/%M")
    date_time = now.strftime("%Y%m%d_%H%M%S")

    cam_client = CamClient(CAM_IP, CAM_USER, CAM_PASS)
    illuminance = cam_client.get_lux()

    if illuminance > LUX_MIN:
        os.makedirs(folder_name, exist_ok=True)
        cam_client.download_img(f"{folder_name}/{date_time}_exp_auto.jpg")
        for exp in exposure_times[:6]:
            cam_client.set_exposure(exp_api_dict.get(exp))
            time.sleep(2)
            cam_client.download_img(f"{folder_name}/{date_time}_exp_{exp}.jpg")
        cam_client.reset_factory_exposure()
        local_files = glob.glob("**/*.jpg", recursive=True)
        uploaded = upload_files(local_files)
        delete_local_files(uploaded)
        delete_empty_dirs(uploaded)
    else:
        logger.warning(f"Illuminance < {LUX_MIN}, skipped.")

    logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
