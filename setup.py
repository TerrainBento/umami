#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(
    name="umami",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="umami landscape metrics",
    url="https://github.com/TerrainBento/umami/",
    author="The TerrainBento Team",
    author_email="barnhark@colorado.edu",
    license="MIT",
    long_description=open("README.md").read(),
    zip_safe=False,
    packages=find_packages(),
    package_data={"": ["tests/*txt", "data/*txt", "data/*asc", "data/*nc"]},
)
