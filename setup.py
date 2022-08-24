# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="ttsMetaClean",
    version="0.3.1",
    description="A text meta-data cleaner for TTS systems.",
    long_description=readme,
    author="Marco Lustri",
    author_email="thelustriva@gmail.com",
    url="https://github.com/TheLustriVA/ttsMetaClean",
    license=license,
    packages=find_packages(exclude=("tests", "docs"))
)
