# -*- coding: utf-8 -*-
# pylint: disable=C0322,C0323
import __pkginfo__
_allowedNames = set(['__name__', '__file__', '__doc__'])
_ignoredNames = set()

# Ignore everything else that's been set up so far, except for the allowed names
_ignoredNames = set(locals().keys()) - _allowedNames

from color import *

__author__ = __pkginfo__.author
__version__ = __pkginfo__.version
__license__ = __pkginfo__.license
__package__ = __name__ = __pkginfo__.modname
__doc__ = __pkginfo__.long_desc

# Add all of the imports, except for the ignored names
__all__ = sorted(set(locals().keys()) - _ignoredNames)
del _allowedNames
del _ignoredNames

if __name__ == '__main__':
    print __pkginfo__.long_desc
