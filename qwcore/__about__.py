NAME = 'qwcore'
ORG = 'qwcode'
VERSION = '0.1.0'
DESCRIPTION = 'Core utils for qwcode projects'
DESCRIPTION_RST = 'Core utils for `qwcode <https://github.com/qwcode>`_ projects.'
AUTHOR = 'Marcus Smith'
EMAIL = 'qwcode@gmail.com'
URL = 'https://github.com/{org}/{name}'.format(name=NAME, org=ORG)
KEYWORDS = 'qwcode utils click logging'
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4'
],
INSTALL_REQUIRES = [
    'setuptools',
    'colorama',
    'invoke',
    'click',
]
ENTRY_POINTS = {}
