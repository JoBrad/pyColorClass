# -*- coding: utf-8 -*-
# pylint: disable=I0011,W0622
# I0011: I0011: Locally disabling
# W0622: W0622: Redefining built-in
"""Packaging information"""
import os

if '__file__' in locals():
    parentDir = os.path.basename(os.path.dirname(__file__))
    modname = distname = parentDir
    __doc__ = '%s %s' % (parentDir, __doc__)

changelog = {
    '0.0.1': [
        'Initial Release'
    ],
    '0.0.2': [
        'Fixed a bug where COLOR constants could be overwritten after assigning them to a variable'
    ],
    '0.0.3': [
        'Separated the definedColors and helpers modules',
        'Refactored code to reduce dependencies, and provide more robust parsing of values',
        'Test coverage is nearly complete!'
    ]
}

# Set the numversion to the latest version in the changelog
numversion = tuple(sorted(changelog.keys()).pop().split('.'))
version = '.'.join([str(num) for num in numversion])

license = 'MIT'
description = 'This module provides a Color class.'
author = 'Joseph T. Bradley'
author_email = 'jtbradley@gmail.com'

classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3'
              ]

long_desc = '''
 This module provides a color class that can store a color value and return it
 in either hex or RGB formats. Conversion between formats is also supported.
 Additionally, named colors (as specified by W3 schools) are built-in, available
 via the COLORS variable.
 .
 All of these functions and methods should work the same regardless of the OS
 that the user is running.
 .
 Additional functions or methods may be added at a later date, as needed.
'''
