"""
up: Upstanding Server Management Support Tools
==============================================

Setup Configuration Script
"""

import codecs
import os
from distutils.core import setup

cwd = os.path.abspath( os.path.dirname( __file__ ) )
rdm = os.path.join( cwd, 'README.md' )

with codecs.open( rdm, encoding = 'utf-8' ) as fh:
    long_description = fh.read()

setup(

    name             = 'up',
    version          = '0.0.0',
    url              = 'https://github.com/zhester/up',
    author           = 'Zac Hester',
    author_email     = 'zac.hester@gmail.com',
    license          = 'BSD 2-Clause',
    description      = 'Upstanding Server Management Support Tools',
    long_description = long_description,

    ### ZIH : test these
    packages         = [ 'up' ],
    scripts          = [ 'scripts/up' ],
    data_files       = [ ( '/usr/local/etc', [ 'data/up.conf.example' ] ) ]

)
