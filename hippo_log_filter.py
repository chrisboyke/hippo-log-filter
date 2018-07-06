#!/usr/bin/env python3
'''
hippo_log_filter.py

Filter the log output from hippo CMS to make it more readable & colorize
different log-levels (INFO, WARN, ERROR, etc.)

Usage:  
    mvn -Pcargo.run | hippo_log_filter.py

Author:
    Chris Boyke chris.boyke@bloomreach.com

'''
import sys, re
from colorama import Fore, Style

VERBOSE = False
WRITE_UNFILTERED=True

# Try to clean up junk in the log file
bad_strings = {'[WARNING] [talledLocalContainer] %d{HH:mm:ss} WARN' : '[WARNING]',
               '[INFO] [talledLocalContainer]' : ''}

# Hippo uses a variety of open-source packages, each of which specifies its own
# log output format, so we try to parse the most common variants, and re-format
# to a more uniform output format...

# Example: 02-Jun-2018 10:08:01.123 INFO ...
dtpattern=r'\s*\d\d-\w\w\w-\d\d\d\d\s+(\d\d:\d\d:\d\d.\d\d\d)\s+(\w+)\s+(.*)'

# Example: 06.02.2018 10:08:01 INFO ...
dtpattern2=r'\s*\d\d\.\d\d\.\d\d\d\d\s+(\d\d:\d\d:\d\d)\s+(\w+)\s+(.*)'

# Example: 10:08:01 WARN ...
timepattern=r'\s*(\d\d:\d\d:\d\d)\s+(\w+)\s+(.*)'

# Example: [INFO] ...
nodtpattern=r'\s*\[(\w+)\]\s*(.*)'

# Example: [2018-06-02T10:08:01,123][INFO] ...
oepattern=r'\[\d\d\d\d-\d\d-\d\dT(\d\d:\d\d\:\d\d,\d\d\d)\]\[(\w+)\s*\]\s*(.*)'

def main():
    print('\n\n' + Fore.GREEN)
    print('hippo_log_filter.py version 1.1 Author chris.boyke@bloomreach.com')
    print('-----------------------------------------------------------------\n\n' + Style.RESET_ALL)

    if WRITE_UNFILTERED:
        f = open('unfiltered.out','w')

    for line in sys.stdin:
        verbose('original')
        verbose(line)
        if WRITE_UNFILTERED:
            f.write(line)
            f.flush()

        type = 'INFO'
        time=''
        line = line.strip()
        for b in bad_strings.keys():
            if b in line:
                verbose('removing',b)
                line = line.replace(b,bad_strings[b])

        m = re.match(dtpattern,line)
        if m:
            verbose('match dtpattern')
            time = m.group(1)
            type = m.group(2)
            line = m.group(3)
        else:
            m = re.match(dtpattern2,line)
            if m:
                verbose('match dtpattern2')
                time = m.group(1)
                type = m.group(2)
                line = m.group(3)
            else:
                m = re.match(timepattern,line)
                if m:
                    verbose('match timepattern')
                    time = m.group(1)
                    type = m.group(2)
                    line = m.group(3)
                else:
                    m = re.match(oepattern,line)
                    if m:
                        verbose('match oepattern')
                        time = m.group(1)
                        type = m.group(2)
                        line = m.group(3)
                    else:
                        m = re.match(nodtpattern,line)
                        if m:
                            verbose('match nodtpattern')
                            type = m.group(1)
                            line = m.group(2)
                        else:
                            verbose('no match')

        color = Fore.BLACK
        if type == 'INFO':
            color = Fore.GREEN
        else:
            if type == 'WARN' or type == 'WARNING':
                color = Style.BRIGHT + Fore.YELLOW
            else:
                if type == 'ERROR':
                    color = Fore.RED
                else:
                    color = Fore.BLUE

        line = line.strip()
        if time:
            time = ' ' + time
        if line:
            print(color + '[' + type + ']'  + Style.RESET_ALL + time + ' ' + line)


def verbose(*args):
	if VERBOSE:
		print(*args)

if __name__ == "__main__":
	main()
