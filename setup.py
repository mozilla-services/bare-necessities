#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements/defaults.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bare-necessities",
    version="0.0.1",
    description="Example minimalist web api",
    author="The Mozilla Team",
    url="https://bare-necessities.herokuapp.com/",
    package_dir={"": "src"},
    packages=find_packages("api"),
    include_package_data=True,
    package_data={"": [""]},
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: Mozilla Public License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
