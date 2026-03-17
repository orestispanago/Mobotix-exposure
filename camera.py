import requests
from requests.auth import HTTPDigestAuth

exposure_times = [
    "1_16000",
    "1__8000",
    "1__4000",
    "1__2000",
    "1__1000",
    "1___500",
    "1___250",
    "1____90",
    "1____60",
    "1____30",
    "1____10",
    "1____5",
    "1____3",
    "1____2",
    "1____1",
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
        url = f"http://{self.ip}/cgi-bin/image.jpg?imgprof=LAPUP_CUSTOM"
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

    def get_text(self):
        return requests.get(f"http://{self.ip}/control/camerainfo?text").text

def extract_lux(data):
    lines = data.strip().split('\n')
    for line in lines:
        if line.startswith("Illumination"):
            label, value, units = line.split()
    return float(value)