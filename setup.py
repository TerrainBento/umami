#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(
    name="umami",
    python_requires=">=3",
    version=versioneer.get_version(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    cmdclass=versioneer.get_cmdclass(),
    description="Umami calculates landscape metrics",
    url="https://github.com/TerrainBento/umami/",
    author="Katy Barnhart",
    author_email="barnhark@colorado.edu",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    packages=find_packages(),
    install_requires=["scipy", "numpy", "landlab>=1.10.1"],
)
