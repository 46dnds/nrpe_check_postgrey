#! /usr/bin/env python

__author__ = ""

__version__= "1.0.0"

'''
* cron * * * * * python /usr/lib/nagios/plugins/check_greylist.py --cron 1
Script to check the postfix server greylist, and warn if an abnormal number of greylisted mail occurs, indicating probable misconfiguration 

Creation date: 09/03/2018
Date last updated: 09/03/2018

* 
* License: GPL
* 
* Description:
* 
* This file contains the check_greylist plugin
* 
* Use the nrpe program to check request on remote server.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
from optparse import OptionParser

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3
cntFile = "/var/cache/postgrey.count"
connection=0

if os.path.isfile(cntFile):
    cfile = open(cntFile, "r")
    connection=int(cfile.read())
    cfile.close()


def check(opts):
    critical = opts.crit
    warning = opts.warn
    if critical and warning:
        if connection > critical:
            print('CRITICAL - The host postfix has %s greylisted connections' %connection)
            sys.exit(ExitCritical)
        elif connection > warning:
            print('WARNING - The host postfix has %s greylisted connections' %connection)
            sys.exit(ExitWarning)
        else:
            print("OK - The host postfix has %s greylisted connections" %connection)
            sys.exit(ExitOK)
    else:
        print("UNKNOWN - The number of greylisted connections is unknown")
        sys.exit(ExitUnknown)    
def main():
    parser = OptionParser("usage: %prog [options] ARG1 ARG2 FOR EXAMPLE: -c 40 -w 10")
    parser.add_option("-C","--cron", dest="cron", help="cron job")
    parser.add_option("-c","--critical", type="int", dest="crit", help="the value if consider very heigth connection in web server")
    parser.add_option("-w","--warning", type= "int", dest="warn", help="the value if consider heigth connection in web server")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    (opts, args) = parser.parse_args()
   
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_greylist.py %s"%__version__)
        sys.exit()


    if opts.cron:
        file = open(cntFile, "w")
        cmdRtn=os.popen("cat /var/log/mail.log | postgreyreport | head -n20 | wc -l").read()
        file.write(cmdRtn)
        file.close()
        sys.exit()

    if opts.crit and opts.warn:
        if opts.crit < opts.warn:
            print("Critical value < Warning value, please check you config")
            sys.exit(ExitCritical)
    else:
        parser.error("Please, this program requires -c and -w arguments, for example: -c 40 -w 10")  
        sys.exit(ExitCritical)

    check(opts)

if __name__ == '__main__':
    main()

  
