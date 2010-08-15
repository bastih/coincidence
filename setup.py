import os
import sys
from setuptools import setup, find_packages

import coincidence

requires = ['unittest2', 'nose']

try:
    import multiprocessing
except ImportError:
    requires += ['multiprocessing']

if sys.version_info < (2, 4):
    print 'ERROR: atp requires at least Python 2.4 to run.'
    sys.exit(1)

setup(
    name='coincidence',
    version=coincidence.__VERSION__,
    license='MIT',
    author='Sebastian Hillig',
    author_email='sebastian.hillig@gmail.com',
    description='Coincidence is a set of tools that can be used to test concurrent operations',
    long_description='',
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Alpha',
    ],
    platforms='any',
    packages=find_packages(),
    install_requires=requires,
)
