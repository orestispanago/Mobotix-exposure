import requests
from requests.auth import HTTPDigestAuth


cam_ip = "YourCameraIP"
cam_user = "YourCameraUsername"
cam_pass = "YourCameraPassword"


def get_digest_auth(url, username, password):
    return requests.get(url, auth=HTTPDigestAuth(username, password))


def download_img(fname):
    url = f"http://{cam_ip}/cgi-bin/image.jpg"
    resp = get_digest_auth(url, cam_user, cam_pass)
    if resp.status_code == 200:
        with open(fname, "wb") as f:
            f.write(resp.content)
    else:
        print(resp.status_code)


def reset_factory():
    url = f"http://{cam_ip}/control/control/?factory&section=exposure"
    get_digest_auth(url, cam_user, cam_pass)


def set_exposure_max(value):
    url = f"http://{cam_ip}/control/control/?set&section=exposure&ca_exp_max={value}"
    get_digest_auth(url, cam_user, cam_pass)


exp_max = 640
set_exposure_max(exp_max)
download_img(f"exp_{exp_max}.png")

exp_max = 160000
set_exposure_max(exp_max)
download_img(f"exp_{exp_max}.png")
