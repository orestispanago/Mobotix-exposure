import datetime
import os
import shutil

from camera import CamClient
from nas import FTPClient


cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

ftp_ip = "YourFTPIP"
ftp_user = "YourFTPUsername"
ftp_password = "YourFTPPassword"
ftp_share = "YourFTPShare"

cam_client = CamClient(cam_ip, cam_user, cam_pass)


def make_dirs_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def set_exposure_max_and_download(exp_max):
    cam_client.set_exposure_max(exp_max)
    cam_client.download_img(f"{local_folder}/{now.strftime('%H%M')}_exp_{exp_max}.png")


now = datetime.datetime.now()
local_folder = now.strftime("%Y/%m/%d")
make_dirs_if_not_exist(local_folder)

set_exposure_max_and_download(640)
set_exposure_max_and_download(160000)

with FTPClient(ftp_ip, ftp_user, ftp_password, ftp_share) as ftp_client:
    ftp_client.upload_folder(local_folder)

shutil.rmtree(local_folder)
