#!/usr/bin/python

from setuptools import setup, find_packages

about = {}
with open("qwcore/__about__.py") as fp:
    exec(fp.read(), about)

with open("readme.rst") as fp:
    long_description = fp.read()

setup(name=about['NAME'],
      version=about['VERSION'],
      description=about['DESCRIPTION'],
      long_description=long_description,
      author=about['AUTHOR'],
      author_email=about['URL'],
      url=about['URL'],
      keywords=about['KEYWORDS'],
      classifiers=about['CLASSIFIERS'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=about['INSTALL_REQUIRES'],
      entry_points=about['ENTRY_POINTS'])
