#!/usr/bin/python3
"""
This Fabric script distributes an archive to my web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["54.237.103.132", "54.197.127.130"]
env.user = "ubuntu"


def do_pack():
    """
        return the archive path if archive has generated correctly.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None


def do_deploy(archive_path):
    """
        Distribute archive.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_dir = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_dir))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             new_dir))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_dir,
                                                new_dir))
        run("sudo rm -rf {}/web_static".format(new_dir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_dir))

        print("New version deployed!")
        return True

    return False
