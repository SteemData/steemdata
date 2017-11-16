import sys
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

assert sys.version_info[0] == 3, "steemdata requires Python > 3"

VERSION = '2.3'

setup(
    name='steemdata',
    version=VERSION,
    description='Python Utilities for parsing STEEM blockchain',
    long_description=open('README.md').read(),
    url='https://github.com/SteemData/steemdata',
    author='@furion',
    author_email='_@furion.me',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='steem',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'pymongo',
        'python-dateutil',
        'requests',
        'funcy',
        'werkzeug',
    ],
    dependency_links=[
        'git+git://github.com/Netherdrake/steem-python'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
