# Setup module for local_climate_change_tool


import sys
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()


# Give setuptools a hint to complain if it's too old a version
# 24.2.0 added the python_requires option
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 24.2.0']
PYTHON_REQUIRES = '>= 3.5'

NAME = 'local_climate_change_tool'
MAINTAINER = 'Claire Zarakas'
MAINTAINER_EMAIL = 'czarakas@uw.edu'
DESCRIPTION = """
This local climate change tool displays the data from CMIP-6
output for historical and 4 different future scenarios via
the Shared Socioeconomic Pathways (SSPs) described below.
The motivation for this tool is to make climate data more
accessible to people with little to no computing knowledge or
background in atmospheric science or climate studies.
"""
LONG_DESCRIPTION = open('README.md').read()
URL = 'https://github.com/czarakas/local_climate_change_tool.git'
DOWNLOAD_URL = 'https://github.com/czarakas/local_climate_change_tool.git'
LICENSE = 'MIT Licence'
VERSION = '1.0'

with open('requirements.txt') as f:
    REQUIRES = f.read().splitlines()

# REQUIRES = ['dask==2.8.1', 'numpy==1.17.3', 'pandas==0.25.3', 'pandocfilters==1.4.2', 
# 'panel==0.7.0', 'param==1.9.2', 'hvplot==0.5.2', 'jupyter-client', 'jupyter-core==4.6.1', 
# 'jupyterlab==1.2.3', 'jupyterlab-server==1.0.6', 'google-api-python-client==1.7.11', 
# 'google-auth==1.7.1', 'google-auth-httplib2==0.0.3','bokeh==1.4.0', 
# 'ipykernel==5.1.3', 'ipython==7.10.1', 'ipython-genutils==0.2.0', 
# 'oauth2client', 'xarray==0.14.1', 'zarr==2.3.2']


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
            install_requires=REQUIRES,
            )

if __name__ == '__main__':
    setup(**opts)
