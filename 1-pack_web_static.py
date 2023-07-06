#!/usr/bin/python3
"""run local commands"""
from fabric.api import loca
from datetime import date
from time import strftime


def do_pack():
    """Create a .tgz archive for our hbnb project
       This is to aid easy deployment
    """
    try:
        current_time = strftime('%Y%m%d%H%m%s')
        local('mkdir -p ./versions')
        local('tar -cvzf ./versions/web_static_{}.tgz ./web_static'
              .format(current_time))
        return './versions/web_static_{}.tgz'.format(current_time)
    except Exception as e:
        return None
