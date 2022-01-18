import datetime
import os
import shutil

from camera import CamClient, exp_api_dict
from nas import FTPClient

cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

ftp_ip = "YourFTPIP"
ftp_user = "YourFTPUsername"
ftp_password = "YourFTPPassword"
ftp_share = "YourFTPShare"


now = datetime.datetime.utcnow()
local_folder = now.strftime("%Y/%m/%d")
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

cam_client = CamClient(cam_ip, cam_user, cam_pass)

exposure_values = ["1_16000", "1_4000", "1_2000", "1_500", "1_250"]

for exp in exposure_values:
    cam_client.set_exposure(exp_api_dict.get(exp))
    cam_client.download_img(f"{local_folder}/{now.strftime('%H%M')}_exp_{exp}.png")
cam_client.reset_factory()

with FTPClient(ftp_ip, ftp_user, ftp_password, ftp_share) as ftp_client:
    ftp_client.upload_folder(local_folder)

shutil.rmtree(local_folder)
