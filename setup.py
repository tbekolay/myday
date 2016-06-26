#!/usr/bin/env python
import io

from setuptools import find_packages, setup


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name="myday",
    version="0.1.0",
    author="Trevor Bekolay",
    author_email="tbekolay@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url="https://github.com/tbekolay/myday",
    description="What should I do with my day?",
    long_description=read('README.rst'),
    entry_points={
        'console_scripts': [
            'myday = myday.main:main',
        ]
    },
    install_requires=[
        'click',
    ],
)
