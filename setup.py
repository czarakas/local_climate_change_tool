# Setup module for Local-Climate-Data-Tool


import sys
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()


# Give setuptools a hint to complain if it's too old a version
# 24.2.0 added the python_requires option
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 24.2.0']

opts = dict(name='Local-Climate-Data-Tool',
            maintainer='Claire Zarakas',
            maintainer_email='czarakas@uw.edu',
            description=
            """
            This local climate data tool displays the data from CMIP-6
            output for historical and 4 different future scenarios via
            the Shared Socioeconomic Pathways (SSPs) described below.
            The motivation for this tool is to make climate data more
            accessible to people with little to no computing knowledge or
            background in atmospheric science or climate studies.
            """,
            long_description=open('README.md').read(),
            url='https://github.com/czarakas/local-climate-data-tool',
            download_url='https://github.com/czarakas/local-climate-data-tool/archive/master.zip',
            license='MIT Licence',
            # classifiers="CLASSIFIERS",
            # author='Ax/Wx"',
            # author_email='axwx@googlegroups.com',
            version='0.1.0',
            packages=PACKAGES,
            # package_data={'axwx': ['data/*', 'data/test_wu_data/*']},
            install_requires=[
            'xarray',
            'pandas',
            'numpy',
            'glob',
            ],
            # requires="REQUIRES"
        )

if __name__ == '__main__':
    setup(**opts)
