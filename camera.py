import requests
from requests.auth import HTTPDigestAuth

exposure_times = [
    "1_16000",
    "1_8000",
    "1_4000",
    "1_2000",
    "1_1000",
    "1_500",
    "1_250",
    "1_90",
    "1_60",
    "1_30",
    "1_10",
    "1_5",
    "1_3",
    "1_2",
    "1_1",
]
api_values = [
    80,
    160,
    320,
    640,
    1280,
    2560,
    4960,
    10080,
    20000,
    40000,
    80000,
    160000,
    320000,
    640000,
    1280000,
]
exp_api_dict = dict(zip(exposure_times, api_values))


class CamClient:
    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.user = user
        self.passwd = passwd

    def get_digest_auth(self, url):
        return requests.get(url, auth=HTTPDigestAuth(self.user, self.passwd))

    def download_img(self, fname):
        url = f"http://{self.ip}/cgi-bin/image.jpg?display_mode=simple"
        resp = self.get_digest_auth(url)
        if resp.status_code == 200:
            with open(fname, "wb") as f:
                f.write(resp.content)
        else:
            print(resp.status_code)

    def reset_factory(self):
        url = f"http://{self.ip}/control/control/?factory&section=exposure"
        self.get_digest_auth(url)

    def set_exposure(self, value):
        url = f"http://{self.ip}/control/control/?set&section=exposure&ca_exp_max={value}&ca_exp_min={value}"
        self.get_digest_auth(url)
