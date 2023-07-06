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

def play():
    run('ls')
    return True
