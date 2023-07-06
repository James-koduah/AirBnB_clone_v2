#!/usr/bin/python3
""" A module to create an archive of web_static """
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """ Create an archive of the webstatic of our hbnb project more words"""
    da = strftime("%Y%m%d%H%m%s")
    try:
        local("mkdir -p ./versions")
        local("tar -cvzf ./versions/web_static_{}.tgz ./web_static"
              .format(da))

        return "versions/web_static_{}.tgz".format(da)

    except Exception as e:
        return None
