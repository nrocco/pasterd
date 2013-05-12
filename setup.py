#!/usr/bin/env python
from setuptools import setup

from pasterd import VERSION

setup(
    name = 'pasterd',
    version = VERSION,
    packages = [
        'pasterd'
    ],
    url = 'http://nrocco.github.io/',
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    description = 'A collection of command line scripts written '
                  'in Python for mutt (and davmail)',
    include_package_data = True,
    install_requires = [
        'bottle',
        'bottle-sqlite',
        'pycli_tools>=1.3'
    ],
    entry_points = {
        'console_scripts': [
            'pasterd = pasterd.webserver:main'
        ]
    },
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
