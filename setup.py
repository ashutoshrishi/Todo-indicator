#!/usr/bin/env python

from distutils.core import setup

files = ["todoapp/*"]

setup ( name = "appname",
        version = "100",
        description = "yadda yadda",
        author = "myself and I",
        author_email = "test@tasd.com",
        url = "whatever",
        packages = ['todoapp'],
        package_data = {'todoapp':files},
        scripts = ['runner'],
        long_description = """Really looooooooooong"""
)


