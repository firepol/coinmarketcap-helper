#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'coinmarketcap-helper',
    packages = ['coinmarketcap_helper'],
    version = '2.0.0',
    description = 'Python wrapper around the coinmarketcap.com API allowing also to query prices by symbol.',
    author = 'firepol',
    author_email = '1702718+firepol@users.noreply.github.com',
    url = 'https://github.com/firepol/coinmarketcap-helper',
    license = 'Apache v2.0 License',
    install_requires=['coinmarketcap>=5.0.3'],
    keywords = ['cryptocurrency', 'API', 'coinmarketcap','BTC', 'Bitcoin', 'LTC', 'Litecoin', 'XRP', 'Ripple', 'ETH', 'Ethereum '],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description = open('README.md','r').read(),
    long_description_content_type='text/markdown',
)
