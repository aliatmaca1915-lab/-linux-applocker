#!/usr/bin/env python3
"""
Linux AppLocker - Setup Script
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linux-applocker",
    version="1.0.0",
    author="Linux AppLocker Team",
    author_email="",
    description="Professional Application and File Locking System for Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliatmaca1915-lab/-linux-applocker",
    packages=find_packages(),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyGObject>=3.42.0",
        "cryptography>=41.0.0",
        "bcrypt>=4.0.0",
        "SQLAlchemy>=2.0.0",
        "python-daemon>=3.0.0",
        "psutil>=5.9.0",
        "pyinotify>=0.9.6",
        "keyring>=24.0.0",
    ],
    entry_points={
        "console_scripts": [
            "linux-applocker=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "systemd/*"],
    },
)
