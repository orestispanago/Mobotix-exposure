import datetime
import glob
import logging
import logging.config
import os
import shutil
import traceback

from camera import CamClient, exp_api_dict, exposure_times
from config import CAM_IP, CAM_PASS, CAM_USER, FTP_IP, FTP_PASS, FTP_USER
from ftp import upload_files

dname = os.path.dirname(__file__)
os.chdir(dname)

os.makedirs("logs", exist_ok=True)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

FTP_DIR = "/cams/All-Sky/lapup-Q71-exposure"

LUX_MIN = 5000


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
            cam_client.download_img(f"{folder_name}/{date_time}_exp_{exp}.jpg")
        cam_client.reset_factory_exposure()
        local_files = glob.glob("**/*.jpg", recursive=True)
        upload_files(FTP_IP, FTP_USER, FTP_PASS, FTP_DIR, local_files)

        shutil.rmtree(folder_name)
    else:
        logger.warning(f"Illuminance < {LUX_MIN}, skipped.")

    logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
