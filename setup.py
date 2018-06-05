#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='esgf_feedback',
      version="0.0.1",
      description='ESGF Email Sender Module',
      author='Sasha Ames',
      author_email='sasha@llnl.gov',
      url='https://github.com/ESGF/esgf-feedback',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=2.7, <3.0',
      platforms=['Unix'],
      zip_safe=False,
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Natural Language :: English',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Build Tools']
      )
