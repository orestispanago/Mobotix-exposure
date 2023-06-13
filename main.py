import datetime
import os
import shutil

from camera import CamClient, exp_api_dict, exposure_times
from nas import FTPClient

cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

ftp_ip = "YourFTPIP"
ftp_user = "YourFTPUsername"
ftp_password = "YourFTPPassword"
ftp_share = "YourFTPShare"


now = datetime.datetime.utcnow()
folder_name = now.strftime("%Y%m%d_%H%M%S")
date_time = now.strftime("%Y%m%d_%H%M%S")
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

cam_client = CamClient(cam_ip, cam_user, cam_pass)

for exp in reversed(exposure_times):
    cam_client.set_exposure(exp_api_dict.get(exp))
    cam_client.download_img(f"{folder_name}/{date_time}_exp_{exp}.png")
cam_client.reset_factory()

with FTPClient(ftp_ip, ftp_user, ftp_password, ftp_share) as ftp_client:
    ftp_client.upload_folder(folder_name)

# shutil.rmtree(folder_name)
