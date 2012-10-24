#!/usr/bin/python
import argparse
import re

parser = argparse.ArgumentParser(
    description='Parse the source Ruby program and analyze its lexical correctness')
parser.add_argument(
    '--source', metavar='str', nargs='+', type=str,
    help='A source to analyze', required=True)

args = parser.parse_args()
for filename in args.source:

    sourcefile = filename
    if re.search(".rb", sourcefile):
        print "\n"
        print 'Ruby source file:', sourcefile
        source = file(sourcefile,'r')
        ln = 1
        while True:
        	line = source.readline()
        	if not line: break
        	print 'ln', ln, ':', line,
        	ln += 1
        source.close()

    else:
        print sourcefile, "is not a valid ruby source"