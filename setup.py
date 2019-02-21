#!/usr/bin/env python
import imp
import io
import os
import sys

from setuptools import find_packages, setup


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

root = os.path.dirname(os.path.realpath(__file__))
version_module = imp.load_source(
    'version', os.path.join(root, 'myday', 'version.py'))
testing = bool({'pytest', 'test'}.intersection(sys.argv))

setup(
    name="myday",
    version=version_module.version,
    author="Trevor Bekolay",
    author_email="tbekolay@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url="https://github.com/tbekolay/myday",
    license="MIT license",
    description="What should I do with my day?",
    long_description=read('README.rst', 'CHANGES.rst'),
    entry_points={
        'console_scripts': [
            'myday = myday:main',
        ]
    },
    setup_requires=["pytest-runner"] if testing else [],
    install_requires=[
        'click',
        'orgmode',
        'python-dateutil',
        'recurrent',
    ],
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
