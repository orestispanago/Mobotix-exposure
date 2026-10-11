## Mobotix-exposure

* Sets Mobotix IP camera exposure time (e.g "1_16000" means 1/1600 seconds)

* Downloads images

* Uploads images folder to FTP server, creating path if necessary

* Deletes local images folder


### Setup

```
sudo apt install python3-dotenv
cp .env.example .env
chmod 600 .env
```

Set the real values in `.env` (FTP and camera credentials), replacing the placeholders. It is in `.gitignore`.
