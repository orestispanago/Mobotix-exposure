import requests
from requests.auth import HTTPDigestAuth
import time


cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"

download_url = f"http://{cam_ip}/cgi-bin/image.jpg"


def get_digest_auth(url, username, password):
    return requests.get(url, auth=HTTPDigestAuth(username, password))


def download_img(url, fname):
    resp = get_digest_auth(url, cam_user, cam_pass)
    if resp.status_code == 200:
        with open(fname, "wb") as f:
            f.write(resp.content)
    else:
        print(resp.status_code)


def reset_factory():
    url = f"http://{cam_ip}/control/control/?factory&section=exposure"
    requests.get(url, auth=HTTPDigestAuth(cam_user, cam_pass))


def set_exposure_max(value):
    url = f"http://{cam_ip}/control/control/?set&section=exposure&ca_exp_max={value}"
    requests.get(url, auth=HTTPDigestAuth(cam_user, cam_pass))


exp_max = 640
start = time.time()
set_exposure_max(exp_max)
exp_interval = time.time()
print(f"Set exposure in: \t{(exp_interval - start):.3f} s")
download_img(download_url, f"exp_{exp_max}.png")
download_interval = time.time()
print(f"Downloaded image in: \t{(download_interval - exp_interval):.3f} s")
set_exposure_max(160000)
exp_interval = time.time()
print(f"Set exposure in: \t{(exp_interval - download_interval):.3f} s")
download_img(download_url, "exp_160000.png")
download_interval = time.time()
print(f"Downloaded image in: \t{(download_interval - exp_interval):.3f} s")
