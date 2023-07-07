#!/usr/bin/python3
""" A module to create an archive of web_static """
from fabric.api import local, env, run, sudo, put
from time import strftime
from datetime import date
import re


env.hosts = ['18.210.17.3', '35.153.232.142']


def do_pack():
    """ Create an archive of the webstatic of our hbnb project more words"""

    da = strftime("%Y%m%d%H%m%s")
    try:
        local("mkdir -p ./versions")
        local("tar -cvzf ./versions/web_static_{}.tgz ./web_static"
              .format(da))

        return "./versions/web_static_{}.tgz".format(da)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """ Unpack the archive in the remote server to host our hbnb page"""
    length = len(archive_path) - 1
    """ Get the file name from the archive path """
    filename = ''
    for i in range(length, 0, -1):
        if archive_path[i-1] == '/':
            filename = archive_path[i:length+1]
            break
    name, ext = filename.split('.')
    try:
        local('echo {}'.format(name))
        put('{}'.format(archive_path), '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(name))
        sudo('rm -r /data/web_static/releases/{}'.format(name))
        sudo('mkdir -p /data/web_static/releases/{}'.format(name))
        sudo('tar -xvzf /tmp/{} -C /data/web_static/releases/{}'
             .format(filename, name))
        sudo('mv /data/web_static/releases/{}/web_static/*\
                /data/web_static/releases/{}'
             .format(name, name))
        sudo('rm -rf /data/web_static/releases/{}/web_static'.format(name))
        sudo('rm -r /tmp/{}'.format(filename))
        sudo('touch /data/web_static/current')
        sudo('rm -r /data/web_static/current')
        sudo('ln -s -f /data/web_static/releases/{} /data/web_static/current'
             .format(name))
        return True
    except Exception as e:
        return False


def deploy():
    """One function that combines both the do_pack and do_deploy as one"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    else:
        safe = do_deploy(archive_path)
        return safe


def do_clean(number=0):
    nn = number
    """delete out-of-date archives counting back with the argument <number>"""
    def clean(dir_path, file_or_dir, number):
        archives = []
        if file_or_dir == 0:
            archives = local(
                    'ls {}'.format(dir_path), capture=True).split('\n')
        else:
            raw = run('ls {}'.format(dir_path))
            raw = re.split(' |\t|\n|\r', raw)
            for i in raw:
                if len(i) > 0 and i[0] == 'w':
                    archives.append(i)
        timestamps = []
        for i in archives:  # Each file in the directory
            length = len(i)
            word = ''
            for c in range(0, length):  # Each character in the filename
                if i[c] == '_' and i[c+1].isnumeric() is True:
                    c = c + 1
                    word = i[c:length]
                    if file_or_dir == 0:
                        numbers, extention = word.split('.')
                        timestamps.append(int(numbers))
                    else:
                        timestamps.append(int(word))
                    break
        if number == 0:
            number = 1
        else:
            number = int(number)
        for i in range(0, number):  # Find the maximum date value
            maximum = 0
            for file_stamp in timestamps:
                if file_stamp > maximum:
                    maximum = file_stamp
            timestamps.remove(maximum)
        for elem in timestamps:
            if file_or_dir == 0:
                filename = 'web_static_{}.tgz'.format(elem)
                local('rm {}/{}'.format(dir_path, filename))
            else:
                dirname = 'web_static_{}'.format(elem)
                sudo('rm -r {}/{}'.format(dir_path, dirname))
    clean('versions', 0, nn)
    clean('/data/web_static/releases', 1, nn)
