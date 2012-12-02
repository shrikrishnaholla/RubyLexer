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
    oplist = ['==','!=','>','>=','<=','<=>','===','.eql?','equal?','+=','-=','*=','/=','%=','**=','<<','>>','&&','||','!','+','-','*','/','=','%','**','<','&','|','^','~']
    punctlist = [',','(',')', '{','}', ':', ';', '.']
    constlist = [str(i) for i in xrange(0,10)]
    # 1: [HOWTO] ensure longest match?
    # 2: [HOWTO] recognize ternary operator ?:
    toklist = []    # List of tokens
    enumlist = []   # Corresponding list to toklist, enumerating the type of the token
    tokidlist = []  # Corresponding list to both toklist and enumlist which contains the unique token id

    @staticmethod
    def idGen(string):
        idnum = 0
        for char in string:
            idnum += ord(char)
        return idnum

    @staticmethod
    def printer(toklist, enumlist, tokidlist, index):
        print toklist[index], '\t\t\t', 
        if enumlist[index] == 0:
            print 'keyword',
        elif enumlist[index] == 1:
            print 'operator',
        elif enumlist[index] == 2:
            print 'constant',
        elif enumlist[index] == 3:
            print 'punctuation',
        else:
            print 'identifier',
        print '\t\t\t\t', tokidlist[index]
        
    @staticmethod
    def classify(lists, string):
        """Classify the token as a keyword, an operator, a punctuation mark, """
        toklist = lists[0]
        enumlist = lists[1]
        tokidlist = lists[2]
        kwlist = lists[3]
        oplist = lists[4]
        punctlist = lists[5]
        constlist = lists[6]
        tokidlist = lists[7]
        done = False
        
        if not string in toklist:                                     # [TODO] Use regexes instead of string comparison
            toklist.append(string)
            for kw in kwlist:                                         # The token is a keywor
                if re.match(re.escape(kw),string):
                    done = True
                    enumlist.append(TokenEnum.keyword)
                    tokidlist.append('KW'+str(SymTab.idGen(string)))
                    break

            if not done:
                for op in oplist:                                         # The token is an operator
                    if re.match(re.escape(op),string):
                        done = True
                        enumlist.append(TokenEnum.operator)
                        tokidlist.append('OP'+str(SymTab.idGen(string)))
                        break
                
            if not done:
                for pn in punctlist:                                      # The token is a punctuation
                    if re.match(re.escape(pn),string):
                        done =True
                        enumlist.append(TokenEnum.punctuation)
                        tokidlist.append('PN'+str(SymTab.idGen(string)))
                        break
            
            if not done:
                for cn in constlist:                                      # The token is a constant
                    if re.match(re.escape(cn),string):
                        done =True
                        enumlist.append(TokenEnum.constant)
                        tokidlist.append('CT'+str(SymTab.idGen(string)))
                        break

                if len(re.findall("'",string)) > 0:
                    enumlist.append(TokenEnum.constant)                   # The token is a string constant
                    tokidlist.append('CT'+str(SymTab.idGen(string)))
                    done = True                         
                    
            if not done:
                    enumlist.append(TokenEnum.identifier)
                    tokidlist.append('ID'+str(SymTab.idGen(string)))

        SymTab.printer(toklist, enumlist, tokidlist, toklist.index(string)) # Print the table



def main():
    parser = argparse.ArgumentParser(
        description='Parse the source Ruby program and analyze its lexical correctness')
    parser.add_argument(
        '--source', metavar='str', nargs='+', type=str,
        help='A source to analyze', required=True)
    
    args = parser.parse_args()
    lists = [SymTab.toklist, SymTab.enumlist, SymTab.tokidlist, SymTab.kwlist, SymTab.oplist, SymTab.punctlist, SymTab.constlist, SymTab.tokidlist]
    
    for filename in args.source:

        sourcefile = filename
        if re.search('.rb$',sourcefile):         # If the sourcefile name ends with '.rb', it's a ruby source file
            print "\n"
            print 'Ruby source file:', sourcefile
            try:
                source = file(sourcefile,'r')
            except IOError:                      # If the input is invalid - file not found
                print sourcefile, "doesn't seem to exist. Please retry"
                continue

            print 'Token','\t\t\t','Type','\t\t\t\t\t','Token ID'
            for x in xrange(0, 50):
                print '-',
            print
            while True:
                tokens =[]
                line = source.readline()               # Read a line from the ruby source file
                if not line: break

                line = re.sub(r'#[^{].*$', "", line)   # Strip out the comments    

                stringlist = re.findall(r'\"(.+?)\"',line)  # Creates a list of string literals
                constlist =[]
                for constr in stringlist:
                    line = line.replace(str(constr), '')
                    # need to detect the pattern #{xyz} and |xyz| inside string literals

                    # detection of #{xyz}
                    strids = re.findall(r'#\{[a-zA-Z]*\}',constr)
                    if type(strids) == list and len(strids) > 0:
                        for var in strids:
                            var, count = re.subn(r'#[{]', '', var)
                            var, count = re.subn(r'[}]', '', var)             # Strip out the unnecessary enclosing characters
                            constr, count = re.subn(r'#[{][a-zA-Z]*[}]', '<var>', constr)          # Remove the to-be-replaced variables from the string literal
                            tokens.append(var)
                            
                    const = "'"+str(constr)+"'"
                    constlist.append(const)                 # Recognizing string literals

                line = line.replace('""','')                # Removing junk double quotes from the stripped line
                tokens += constlist

                #Detection of |xyz|
                varids = re.findall(r'\|[a-zA-Z]*\|',line)
                if len(varids) > 0:
                    for var in varids:
                        line = line.replace(var,'')
                        tok, count = re.subn(r'[|]', '', var)             # Strip out the unnecessary enclosing characters
                        tokens += tok

                for punct in SymTab.punctlist:
                    line = line.replace(punct,' '+ punct + ' ')

                for optor in SymTab.oplist:
                    line = line.replace(optor,' '+optor+' ')

                tokens += line.split()            # [HOWTO] This splits only on the basis of whitespace characters. Need to remove brackets too

                for token in tokens:
                    SymTab.classify(lists, token)       # Analyzes the tokens
                
            source.close()
    
        else:                                    # If the extension is not '.rb'
            print sourcefile, "is not a valid ruby source"

if __name__ == '__main__':
    main()