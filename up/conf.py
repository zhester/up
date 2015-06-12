#!/usr/bin/env python

"""
Tool Configuration Management

The standard location for user-installed system configuration is
`/usr/local/etc/up.conf`.  This can be changed using this module's attribute
named `confpath`.
"""


import json
import os
import re


__version__ = '0.0.0'


# Path to the configuration file.
confpath = '/usr/local/etc/up.conf'


#=============================================================================
class FileError( IOError ):
    """
    Thrown when there is a problem reading the configuration file.
    """
    pass


#=============================================================================
class ParseError( ValueError ):
    """
    Thrown when there is a problem parsing the configuration file.
    """
    pass


#=============================================================================
class ValidError( ValueError ):
    """
    Thrown when the configuration data is invalid.
    """
    pass


#=============================================================================
def load_conf( path = None, validate = True ):
    """
    Loads the configuration for use by the system.

    @param path Overrides the default path to the configuration file
    @return     The dictionary of configuration values
    @throws     FileError if the config file could not be loaded from disk
    @throws     ParseError if the config file could not be parsed
    @throws     ValidError if the file contains an invalid configuration
    """

    # allow the path to be overridden locally
    path = confpath if path is None else path

    # open the configuration file
    try:
        cfh = open( path, 'r' )
    except IOError:
        raise FileError( 'Unable to open config file {}'.format( path ) )

    # read the config data, and strip comments
    conf = cfh.read()
    cfh.close()
    conf = strip_comments( conf )

    # parse the config file
    try:
        data = json.loads( conf )
    except ValueError:
        raise ParseError( 'Configuration file format is not JSON.' )

    # perform helpful path manipulation/sanitation
    if ( 'back' in data ) and ( 'paths' in data[ 'back' ] ):
        for pair in data[ 'back' ][ 'paths' ]:
            pair[ 0 ] = os.path.expanduser( pair[ 0 ] )
            pair[ 1 ] = os.path.expanduser( pair[ 1 ] )

    # make sure the user needs validation (they should)
    if validate == True:

        # validate basic sanity of config file
        if     (      'up' not in data           ) \
            or ( 'logfile' not in data[ 'up' ]   ) \
            or (    'back' not in data           ) \
            or (   'paths' not in data[ 'back' ] ) :
            raise ValidError( 'Config file sanity check failed.' )

        # validate backup paths
        paths = data[ 'back' ][ 'paths' ]
        for ( source, target ) in paths:
            if ( ':' not in source ) and ( os.path.exists( source ) == False ):
                raise ValidError(
                    'Source "{}" does not exist.'.format( source )
                )
            if ( ':' not in target ) and ( os.path.exists( target ) == False ):
                raise ValidError(
                    'Target "{}" does not exist.'.format( target )
                )

    # if we make it this far, the configuration is good
    return data


#=============================================================================
# Support for comment stripping (see hzpy/modules/comments.py)
_missme = r'(?:(?!(?P=quote))|[^\\\r\n])'
_quotes = '"\'`'
_whites = ' \t\r\n'
_patterns = {
    'dqs' : r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"',
    'sqs' : r"'[^'\\\r\n]*(?:\\.[^'\\\r\n]*)*'",
    'mqs' : r'(?P<quote>[{q}]){m}*(?:\\.{m}*)*(?P=quote)'.format(
        q = _quotes,
        m = _missme
    ),
    'csc' : r'/\*(?:.|[\r\n])*?\*/',
    'ssc' : r'(?://|#).*$',
    'quotes' : _quotes,
    'whites' : _whites
}
_pattern = re.compile(
    '({mqs})|[{whites}]?{csc}[{whites}]?|{ssc}'.format( **_patterns ),
    re.MULTILINE
)


#=============================================================================
def _replacer( match ):
    """
    Replacement function for `re.sub()` callbacks.

    @param match The MatchObject instance for the current match
    @return      The string to use in place of the current match
    """

    # get the entire match string and the first subgroup
    g0, g1 = match.group( 0, 1 )

    # string literal was matched, do not remove it from the subject string
    if g1 is not None:
        return g1

    # C-style comments with no surrounding space are replaced with a space
    #   to allow "BEFORE/* ... */AFTER" to become "BEFORE AFTER"
    if g0.startswith( '/*' ) and g0.endswith( '*/' ):
        return ' '

    # restore optionally-matched surrounding whitespace characters
    replace = ''
    if g0[ 0 ] in _whites:
        replace += g0[ 0 ]
    if g0[ -1 ] in _whites:
        replace += g0[ -1 ]
    return replace


#=============================================================================
def strip_comments( string ):
    """
    Strips all code comments from the given string.

    @param string The string from which to strip comments
    @return       The string minus all comments
    """

    # strip all comments
    return re.sub( _pattern, _replacer, string )


#=============================================================================
def main( argv ):
    """
    Built-in module testing.
    """

    #=========================================================================
    # configuration loading, parsing, validation testing
    project_path = os.path.dirname(
        os.path.dirname( os.path.realpath( __file__ ) )
    )
    test_path = os.path.join( project_path, 'data', 'up.conf' )

    try:
        conf = load_conf( test_path )
    except ValidError as ve:
        print( 'ValidError: {}'.format( ve ) )
    else:
        json.dump( conf, sys.stdout, indent = 2 )
        sys.stdout.write( '\n' )


#=============================================================================
if __name__ == "__main__":
    import sys
    sys.exit( main( sys.argv ) )

