#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

from kerdezo import __version__ as package_version

REQUIREMENTS = [
    l.strip() for l in open("requirements.txt", "r", encoding="utf8").readlines()
]

setup(
    name="kerdezo",
    version=package_version,
    author="fogasl",
    description="Interactive suite for console applications",
    long_description=open("README.md", "r", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fogasl/kerdezo",
    keywords="",
    license="BSD-3-Clause",
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities"
    ]
)
