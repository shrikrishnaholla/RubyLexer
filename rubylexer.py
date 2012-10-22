#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(
    description='Parse the source Ruby program and analyze its lexical correctness')
parser.add_argument(
    '--source', metavar='str', nargs='+', type=str,
    help='A source to analyze')

args = parser.parse_args()
for filename in args.source:
    sourcefile = filename
    print 'Ruby source file:', sourcefile
    source = file(sourcefile,'r')
    ln = 1
    while True:
    	line = source.readline()
    	if not line: break
    	print 'ln', ln, ':', line
    	ln += 1
    print
    source.close()