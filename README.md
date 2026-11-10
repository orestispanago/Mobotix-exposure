## Mobotix-exposure

* Sets Mobotix IP camera exposure time (e.g. "1_16000" means 1/16000 seconds)

* Downloads images

* Uploads images folder to an FTP or SFTP server, creating path if necessary

* Deletes local images after a successful upload. Failed uploads stay local and are retried on the next run


### Setup

```
pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Set the real values in `.env` (server and camera credentials), replacing the placeholders.

### Cronjob

```bash
*/10 * * * * python3 ~/Mobotix-exposure/main.py
```
