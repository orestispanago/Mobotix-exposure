import datetime
import shutil

from camera import CamClient
from nas import FTPClient
from utils import exp_api_dict, make_dirs_if_not_exist

cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

ftp_ip = "YourFTPIP"
ftp_user = "YourFTPUsername"
ftp_password = "YourFTPPassword"
ftp_share = "YourFTPShare"


cam_client = CamClient(cam_ip, cam_user, cam_pass)

now = datetime.datetime.utcnow()
local_folder = now.strftime("%Y/%m/%d")
make_dirs_if_not_exist(local_folder)

exposure_values = ["1_16000", "1_4000", "1_2000", "1_500", "1_250"]

for exp in exposure_values:
    cam_client.set_exposure_max(exp_api_dict.get(exp))
    cam_client.download_img(
        f"{local_folder}/{now.strftime('%H%M')}_exp_{exp}.png")

with FTPClient(ftp_ip, ftp_user, ftp_password, ftp_share) as ftp_client:
    ftp_client.upload_folder(local_folder)

shutil.rmtree(local_folder)
