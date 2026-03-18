from ftplib import FTP, error_perm
import os
import logging

logger = logging.getLogger(__name__)


def upload_file(ftp_session, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp_session.storbinary(f"STOR {remote_path}", f)
    logger.info(f"Uploaded {local_path} to {remote_path}")


def mkdir_and_enter(ftp_session, dir_name):
    if dir_name not in ftp_session.nlst():
        ftp_session.mkd(dir_name)
        logger.debug(f"Created FTP directory {dir_name}")
    ftp_session.cwd(dir_name)


def make_dirs(ftp_session, folder_path):
    for f in folder_path.split("/"):
        mkdir_and_enter(ftp_session, f)


def upload_files(ftp_ip, ftp_user, ftp_password, ftp_dir, local_files):
    with FTP(ftp_ip, ftp_user, ftp_password) as ftp_session:
        ftp_session.cwd(ftp_dir)
        for local_file in local_files:
            local_file = local_file.replace("\\", "/")
            remote_path = local_file
            try:
                upload_file(ftp_session, local_file, remote_path)
            except error_perm as e:
                if "55" in str(e):
                    make_dirs(ftp_session, os.path.dirname(remote_path))
                    ftp_session.cwd(ftp_dir)
                    upload_file(ftp_session, local_file, remote_path)
