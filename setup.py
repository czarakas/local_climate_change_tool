# Setup module for Local-Climate-Data-Tool


import sys
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()


# Give setuptools a hint to complain if it's too old a version
# 24.2.0 added the python_requires option
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 24.2.0']
PYTHON_REQUIRES = '>= 3.5'

NAME = 'Local-Climate-Data-Tool'
MAINTAINER = 'Claire Zarakas'
MAINTAINER_EMAIL = 'czarakas@uw.edu'
DESCRIPTION = """
This local climate data tool displays the data from CMIP-6
output for historical and 4 different future scenarios via
the Shared Socioeconomic Pathways (SSPs) described below.
The motivation for this tool is to make climate data more
accessible to people with little to no computing knowledge or
background in atmospheric science or climate studies.
"""
LONG_DESCRIPTION = open('README.md').read()
URL = 'https://github.com/czarakas/local-climate-data-tool'
DOWNLOAD_URL = 'https://github.com/czarakas/local-climate-data-tool/archive/master.zip'
LICENSE = 'MIT Licence'
VERSION = '0.1.0'
#REQUIRES


opts = dict(name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            version=VERSION,
            packages=PACKAGES,
            python_requires=PYTHON_REQUIRES,
            setup_requires=SETUP_REQUIRES,
            )

if __name__ == '__main__':
    setup(**opts)
