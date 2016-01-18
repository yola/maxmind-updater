#!/usr/bin/env python
from setuptools import setup
import maxmindupdater

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name=maxmindupdater.__name__,
    version=maxmindupdater.__version__,
    description=maxmindupdater.__doc__,
    long_description=readme,
    author='Yola',
    author_email='engineers@yola.com',
    license='MIT (Expat)',
    url=maxmindupdater.__url__,
    packages=['maxmindupdater'],
    test_suite='nose.collector',
    install_requires=[
        'requests >= 2.0.0, < 3.0.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
