# -*- coding: utf-8 -*-
import re
import codecs

from setuptools import setup
from setuptools.command.test import test as TestCommand


class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


setup(
    name = 'pasterd',
    description = 'A collection of command line scripts written in Python for mutt (and davmail)',
    version = re.search(r'''^__version__\s*=\s*["'](.*)["']''', open('pasterd/__init__.py').read(), re.M).group(1),
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    url = 'http://github.com/nrocco/pasterd',
    license = 'GPLv3',
    long_description = codecs.open('README.rst', 'rb', 'utf-8').read(),
    test_suite='nose.collector',
    tests_require = [
        'nose',
        'webtest',
        'mock',
        'coverage',
    ],
    packages = [
        'pasterd'
    ],
    include_package_data = True,
    install_requires = [
        'bottle>=0.12',
        'bottle-sqlite>=0.1.2',
        'pycli-tools>=2.0.1'
    ],
    entry_points = {
        'console_scripts': [
            'pasterd = pasterd.main:main'
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
    cmdclass = {
        'test': NoseTestCommand
    }
)
