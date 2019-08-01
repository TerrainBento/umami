#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(
    name="umami",
    version=versioneer.get_version(),
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
    install_requires=[
        "scipy",
        "numpy",
        "jupyter",
        "holoviews",
        "pandas",
        "landlab>=1.9",
    ],
    package_data={"": ["tests/data/*"]},
)
