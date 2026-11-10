import logging
import posixpath

import paramiko

logger = logging.getLogger(__name__)


def connect(host, port, user, password, known_hosts_file):
    client = paramiko.SSHClient()
    client.load_host_keys(known_hosts_file)
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(
        host,
        port=port,
        username=user,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    return client


def remote_dir_exists(sftp_session, path):
    try:
        sftp_session.stat(path)
        exists = True
    except FileNotFoundError:
        exists = False
    return exists


def make_dirs(sftp_session, folder_path):
    current = ""
    for part in folder_path.split("/"):
        current = posixpath.join(current, part)
        if not remote_dir_exists(sftp_session, current):
            sftp_session.mkdir(current)
            logger.debug(f"Created SFTP directory {current}")


def remove_if_exists(sftp_session, path):
    try:
        sftp_session.remove(path)
    except OSError:
        pass


def upload_file(sftp_session, local_path, remote_path):
    temp_path = f"{remote_path}.part"
    make_dirs(sftp_session, posixpath.dirname(remote_path))
    try:
        sftp_session.put(local_path, temp_path)
        sftp_session.posix_rename(temp_path, remote_path)
    except OSError:
        remove_if_exists(sftp_session, temp_path)
        raise
    logger.info(f"Uploaded {local_path} to {remote_path}")


def upload_files(host, port, user, password, known_hosts_file, sftp_dir, local_files):
    uploaded = []
    client = connect(host, port, user, password, known_hosts_file)
    try:
        sftp_session = client.open_sftp()
        sftp_session.chdir(sftp_dir)
        for local_file in local_files:
            local_file = local_file.replace("\\", "/")
            try:
                upload_file(sftp_session, local_file, local_file)
                uploaded.append(local_file)
            except OSError as e:
                logger.error(f"Could not upload {local_file}: {e}")
    finally:
        client.close()
    return uploaded
