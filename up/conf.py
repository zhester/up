#!/usr/bin/env python

"""
Tool Configuration Management

The standard location for user-installed system configuration is
`/usr/local/etc/up.conf`.  This can be changed using this module's attribute
named `confpath`.
"""


import json
import re


__version__ = '0.0.0'


# Path to the configuration file.
confpath = '/usr/local/etc/up.conf'


#=============================================================================
def load_conf( path = None ):
    """
    Loads the configuration for use by the system.

    @param path Overrides the default path to the configuration file
    @return     The dictionary of configuration values
    @throws     IOError if the config file could not be loaded/parsed
    """

    # allow the path to be overridden locally
    path = confpath if path is None else path

    # read and parse the config file
    with open( path, 'r' ) as cfh:
        conf = cfh.read()
        conf = strip_comments( conf )
        try:
            data = json.loads( conf )
        except ValueError:
            raise IOError( 'Configuration file format is not JSON.' )
        return data


#=============================================================================
def strip_comments( string ):
    """
    Adapted from a great answer on Stack Overflow:
        http://stackoverflow.com/questions/241327/

    @param string The string from which to strip comments
    @return       The string minus all comments
    """

    # first, strip shell-style comments
    string = re.sub( r'^\s*#.*$', '', string, flags = re.MULTILINE )

    # define a replacement function to catch joined C-style comments
    def replacer( match ):
        capture = match.group( 0 )
        if capture.startswith( '/' ):
            return ' '
        return capture

    # compile a pattern to match all C- and C++-style comments
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        ( re.DOTALL | re.MULTILINE )
    )

    # replace all comments
    return re.sub( pattern, replacer, string )


#=============================================================================
def main( argv ):
    """
    Built-in module testing.
    """
    project_path = os.path.dirname(
        os.path.dirname( os.path.realpath( __file__ ) )
    )
    test_path = os.path.join( project_path, 'data', 'up.conf' )
    #print strip_comments( open( test_path, 'r' ).read() )
    conf = load_conf( test_path )
    json.dump( conf, sys.stdout, indent = 2 )
    sys.stdout.write( '\n' )


#=============================================================================
if __name__ == "__main__":
    import os
    import sys
    sys.exit( main( sys.argv ) )

