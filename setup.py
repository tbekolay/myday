#!/usr/bin/env python

import io
import os
import runpy

try:
    from setuptools import find_packages, setup
except ImportError:
    raise ImportError(
        "'setuptools' is required but not installed. To install it, "
        "follow the instructions at "
        "https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py"
    )


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


root = os.path.dirname(os.path.realpath(__file__))
version = runpy.run_path(os.path.join(root, "myday", "version.py"))["version"]

install_req = [
    "click",
    "requests",
]
win_req = [
    "colorama",
]
docs_req = []
optional_req = []
tests_req = [
    "codespell",
    "flake8",
    "gitlint",
    "nengo-bones",
    "pylint",
]

setup(
    name="myday",
    version=version,
    author="Applied Brain Research",
    author_email="info@appliedbrainresearch.com",
    packages=find_packages(),
    # url="https://www.nengo.ai/myday",
    include_package_data=False,
    license="Free for non-commercial use",
    description="Lightweight personal time management",
    long_description=read("README.rst", "CHANGES.rst"),
    zip_safe=False,
    install_requires=install_req,
    extras_require={
        "all": docs_req + optional_req + tests_req,
        "docs": docs_req,
        "optional": optional_req,
        "tests": tests_req,
        ":sys.platform == 'win32'": win_req,
    },
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
    ],
)
