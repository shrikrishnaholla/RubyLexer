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
    if re.search(".rb", sourcefile):         # If the sourcefile contains '.rb', it's a ruby source file
        print "\n"
        print 'Ruby source file:', sourcefile
        try:
            source = file(sourcefile,'r')
        except IOError:                      # If the input is invalid - file not found
            print sourcefile, "doesn't seem to exist. Please retry"
            continue
        ln = 1
        while True:
            line = source.readline()         # Read a line from the ruby source file
            if not line: break
            print 'ln', ln, ':', line,
            ln += 1                          # Increment line number count
            def tokenize(line):
                tokens = line.split()    # Not enough - This splits only on the basis of whitespace characters
                for token in tokens:     # You have the tokens - now you have to analyze them
                    pass
            tokenize(line)
        source.close()

    else:                                    # If the extension is not '.rb'
        print sourcefile, "is not a valid ruby source"