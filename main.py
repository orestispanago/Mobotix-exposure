import datetime
import os
import shutil

from camera import CamClient, exp_api_dict, exposure_times, extract_lux
from nas import FTPClient

cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

ftp_ip = "YourFTPIP"
ftp_user = "YourFTPUsername"
ftp_password = "YourFTPPassword"
ftp_share = "YourFTPShare"

LUX_MIN = 5000 

now = datetime.datetime.now(datetime.timezone.utc)
folder_name = now.strftime("%Y/%m/%d/%H/%M")
date_time = now.strftime("%Y%m%d_%H%M%S")

cam_client = CamClient(cam_ip, cam_user, cam_pass)
data = cam_client.get_text()
illuminance = extract_lux(data)

if illuminance > LUX_MIN:
    os.makedirs(folder_name, exist_ok=True)
    cam_client.download_img(f"{folder_name}/{date_time}_exp_auto.jpg")
    for exp in exposure_times[:6]:
        cam_client.set_exposure(exp_api_dict.get(exp))
        cam_client.download_img(f"{folder_name}/{date_time}_exp_{exp}.jpg")
    cam_client.reset_factory()

    # with FTPClient(ftp_ip, ftp_user, ftp_password, ftp_share) as ftp_client:
    #     ftp_client.upload_folder(folder_name)

    # shutil.rmtree(folder_name)
else:
    print(f"Illuminance < {LUX_MIN}, skipped.")