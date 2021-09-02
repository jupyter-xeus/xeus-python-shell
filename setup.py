#!/usr/bin/env python

from setuptools import setup, find_packages

__AUTHOR__ = 'QuantStack dev team'

setup(
    name='xeus-python-shell',
    version='0.1.4',
    description='The xeus-python core python logic.',
    author=__AUTHOR__,
    maintainer=__AUTHOR__,
    url='https://github.com/jupyter-xeus/xeus-python-shell',
    license='BSD 3-Clause',
    keywords='python ipython xeus-python',
    packages=find_packages(exclude=['test']),
    python_requires='>=3.6',
    install_requires=[
        'ipython>=7.21,<8',
        'debugpy>=1.1.0,<2'
    ],
    extras_require={
        'testing': ['flake8'],
    },
    platforms=['any'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
