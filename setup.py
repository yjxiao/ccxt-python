# prefer setuptools over distutils
from setuptools import setup, find_packages

# use a consistent encoding
from codecs import open
from os import path
import json
import sys

is_python_2 = sys.version_info < (3, 0)

here = path.abspath(path.dirname(__file__))
root = path.dirname(here)

readme = path.join(here, 'README.md')
package_json = path.join(here, 'package.json')

# a workaround when installing locally from git repository with pip install -e .
if not path.isfile(package_json):
    package_json = path.join(root, 'package.json')

# long description from README file
with open(readme, encoding='utf-8') as f:
    long_description = f.read()

# version number and all other params from package.json
with open(package_json, encoding='utf-8') as f:
    package = json.load(f)

project_links = {
    'Homepage': 'https://ccxt.trade',
    'Documentation': 'https://ccxt.readthedocs.io/en/latest/manual.html',
    'Discord': 'https://discord.gg/dhzSKYU',
    'Twitter': 'https://twitter.com/ccxt_official',
    'Funding': 'https://opencollective.com/ccxt',
}

setup(

    name=package['name'],
    version=package['version'],

    description=package['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',

    # will switch from rst to md shortly
    # long_description_content_type='text/markdown',

    url=package['homepage'],

    author=package['author']['name'],
    author_email=package['author']['email'],

    license=package['license'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: JavaScript',
        'Programming Language :: PHP',
        'Operating System :: OS Independent',
        'Environment :: Console'
    ],

    keywords=package['keywords'],
    packages=find_packages(exclude=['ccxt.async_support*'] if is_python_2 else []),

    install_requires=[
        'setuptools>=38.5.1',
        'certifi>=2018.1.18',
        'requests>=2.18.4',
        'cryptography>=2.6.1'
    ],

    extras_require={
        ':python_version>="3.5.2"': [
            'aiohttp>=3.7.4,<3.8',
            'aiodns>=1.1.1,<2.1',
            'yarl==1.6.3',
        ],
        'qa': [
            'flake8==3.7.9',
        ],
        'doc': [
            'Sphinx==4.0',
            'm2r2==0.2.7',
            'sphinx-rtd-theme==0.5.2',
            'readthedocs-sphinx-search==0.1.0',
        ]
    },
    project_links=project_links,
)
