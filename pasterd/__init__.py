# -*- coding: utf-8 -*-
__version__ = '1.3.1'
__usage__ = '''
pasterd                                             v %s

NAME
    pasterd - command line paste bin utility


SYNOPSIS
    <command> | curl -F '%s=<-' %s


DESCRIPTION
    Create a paste:
'''



if '__main__' == __name__:
    from pasterd.webserver import main
    main()
