#!/usr/bin/python3
"""run local commands"""
from fabric.api import *
from datetime import date
from time import strftime

env.user = 'ubuntu'
env.hosts = ['100.25.31.18', '34.232.78.18']


def do_pack():
    """Create a .tgz archive"""
    try:
        current_time = strftime('%Y%m%d%H%m%s')
        local('mkdir -p ./versions')
        local('tar -cvzf ./versions/web_static_{}.tgz ./web_static'
              .format(current_time))
        return './versions/web_static_{}.tgz'.format(current_time)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribute an archive to our web servers"""
    try:
        filename = archive_path.split('/').pop()
        filename_no_extention = filename.split('.')[0]
        put(archive_path, '/tmp/')
        """incase the archive already exists"""
        sudo('mkdir -p /data/web_static/releases/{}'
             .format(filename_no_extention))
        sudo('rm -r /data/web_static/releases/{}'
             .format(filename_no_extention))

        sudo('mkdir -p /data/web_static/releases/{}'
             .format(filename_no_extention))
        sudo('tar -xzvf /tmp/{} -C /data/web_static/releases/{}'
             .format(filename, filename_no_extention))

        """Copy all files from the new sub folder to the main path"""
        sudo('cp -r /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}'
             .format(filename_no_extention, filename_no_extention))
        sudo('rm -rf /data/web_static/releases/{}/web_static/'
             .format(filename_no_extention))

        sudo('rm /tmp/{}'.format(filename))
        sudo('rm /data/web_static/current')
        sudo('ln -sf /data/web_static/releases/{} /data/web_static/current'
             .format(filename_no_extention))
        return True
    except Exception as e:
        print('---------------')
        print('Error')
        print('---------------')
        return False


def deploy():
    """Create a new archive and deploy it
       Create an archive and deploy automatically
    """
    archive = do_pack()
    if archive is None:
        return False
    dep = do_deploy(archive)
    if dep is False:
        return False
    return dep
