#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


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
    install_requires=["Flask==1.1.2", "gunicorn==20.0.4"],
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
