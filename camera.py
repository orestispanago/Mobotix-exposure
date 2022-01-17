import requests
from requests.auth import HTTPDigestAuth


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

    def set_exposure_max(self, value):
        url = (
            f"http://{self.ip}/control/control/?set&section=exposure&ca_exp_max={value}"
        )
        self.get_digest_auth(url)
