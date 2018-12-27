#!/usr/bin/python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pandas-sets',
    version='v0.1.1',
    packages=find_packages(),
    license='BSD',
    description='Pandas - Sets:  Set-oriented Operations in Pandas',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Florents Tselai',
    author_email='florents@tselai.com',
    url='https://github.com/Florents-Tselai/pandas-sets',
    install_requires=open('requirements.txt').read().splitlines()
)
