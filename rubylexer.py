#!/usr/bin/python
import argparse
import re
import random

class TokenEnum(object):
    """TokenEnum is an enumerator of all kinds of tokens available to the Symbol Table"""
    keyword = 0
    operator = 1
    constant = 2
    punctuation = 3
    identifier = 4
        

class SymTab:
    """SymTab is the class holding the Symbol Table as a collection of three lists,
    one containing the tokens, another the type of the token, and the last one holding a unique ID for the token"""
    kwlist = ['BEGIN', 'END', '__ENCODING__', '__END__', '__FILE__', '__LINE__', 'alias', 'and', 'begin', 'break', 'case', 'class', 'def', 'defined?', 'do', 'else', 'elsif', 'end', 'ensure', 'false', 'for', 'if', 'in', 'module', 'next', 'nil', 'not', 'or', 'redo', 'rescue', 'retry', 'return', 'self', 'super', 'then', 'true', 'undef', 'unless', 'until', 'when', 'while', 'yield']
    oplist = ['+','-','*','/','=','%','**','==','!=','>','>=','<','<=','<=>','===','.eql?','equal?','+=','-=','*=','/=','%=','**=','&','|','^','~','<<','>>','&&','||','!']
    punctlist = [',']
    constlist = [str(i) for i in xrange(0,10)]
    # 1: [HOWTO] ensure longest match?
    # 2: [HOWTO] implement ternary operator ?:
    toklist = []    # List of tokens
    enumlist = []   # Corresponding list to toklist, enumerating the type of the token
    tokidlist = []  # Corresponding list to both toklist and enumlist which contains the unique token id
    idlist = []     # List of all unique ids generated

    @staticmethod
    def randomIdGen(idlist):
        while True:
            iden = random.randint(1000,9999)
            if not iden in idlist:
                idlist.append(iden)
                return iden

    @staticmethod
    def printer(toklist, enumlist, tokidlist, index):
        print toklist[index], '\t\t\t', enumlist[index], '\t', tokidlist[index]
        
    @staticmethod
    def classify(lists, string):
        toklist = lists[0]
        enumlist = lists[1]
        tokidlist = lists[2]
        kwlist = lists[3]
        oplist = lists[4]
        punctlist = lists[5]
        constlist = lists[6]
        tokidlist = lists[7]
        idlist = lists[8]
        
        if not string in toklist:
            toklist.append(string)
            if string in kwlist:
                enumlist.append(TokenEnum.keyword)
                tokidlist.append('KW'+str(SymTab.randomIdGen(idlist)))
            elif string in oplist:
                enumlist.append(TokenEnum.operator)
                tokidlist.append('OP'+str(SymTab.randomIdGen(idlist)))
            elif string in punctlist:
                enumlist.append(TokenEnum.punctuation)
                tokidlist.append('PN'+str(SymTab.randomIdGen(idlist)))
            elif string in constlist:
                enumlist.append(TokenEnum.constant)
                tokidlist.append('CT'+str(SymTab.randomIdGen(idlist)))
            else:
                enumlist.append(TokenEnum.identifier)
                tokidlist.append('ID'+str(SymTab.randomIdGen(idlist)))

        SymTab.printer(toklist, enumlist, tokidlist, toklist.index(string))

def main():
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
            print 'Token','\t\t\t','Type','\t','Token ID'
            for x in xrange(0, 35):
                print '-',
            print
            while True:
                line = source.readline()         # Read a line from the ruby source file
                if not line: break
                #print 'ln', ln, ':', line,      # print the line
                ln += 1                          # Increment line number count
                tokens = line.split()            # [HOWTO] This splits only on the basis of whitespace characters. Is it enough?
                for token in tokens:
                    lists = [SymTab.toklist, SymTab.enumlist, SymTab.tokidlist, SymTab.kwlist, SymTab.oplist, SymTab.punctlist, SymTab.constlist, SymTab.tokidlist, SymTab.idlist]
                    SymTab.classify(lists, token)       # Analyzes the tokens
                
            source.close()
    
        else:                                    # If the extension is not '.rb'
            print sourcefile, "is not a valid ruby source"

if __name__ == '__main__':
    main()