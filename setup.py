#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='google-scholar-scraper',
      version='0.1',
      description='Python library for scraping Google Scholar.',
      long_description=long_description,
      author='Adeel Khan',
      author_email='kadeel@gmail.com',
      license='GPL',
      url='http://github.com/adeel/google-scholar-scraper',
      package_dir={'': 'src'},
      py_modules=['gsscraper'],
      entry_points={
        'console_scripts': [
          'gsscraper=gsscraper:main'
        ]
      },
      install_requires=['requests', 'bibtexparser'],
      dependency_links=[
        'git+http://git@github.com/sciunto/python-bibtexparser.git#egg=bibtexparser-0.5.5git'
      ],
      keywords='references citations bibliography'
)
