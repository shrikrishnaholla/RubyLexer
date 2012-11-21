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
    punctlist = [',','\"','(',')','{','}','#' '?', ':', ';']
    constlist = [str(i) for i in xrange(0,10)]
    # 1: [HOWTO] ensure longest match?
    # 2: [HOWTO] recognize ternary operator ?:
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
        idlist = lists[8]
        
        if not string in toklist:                                     # [TODO] Use regexes instead of string comparison
            toklist.append(string)
            if string in kwlist:                                      # The token is a keyword
                enumlist.append(TokenEnum.keyword)
                tokidlist.append('KW'+str(SymTab.randomIdGen(idlist)))
            elif string in oplist:                                    # The token is an operator
                enumlist.append(TokenEnum.operator)
                tokidlist.append('OP'+str(SymTab.randomIdGen(idlist)))
            elif string in punctlist:                                 # The token is a punctuation
                enumlist.append(TokenEnum.punctuation)
                tokidlist.append('PN'+str(SymTab.randomIdGen(idlist)))
            elif string in constlist:                                 # The token is a constant
                enumlist.append(TokenEnum.constant)
                tokidlist.append('CT'+str(SymTab.randomIdGen(idlist)))
            else:                                                     # The token is an identifier
                enumlist.append(TokenEnum.identifier)
                tokidlist.append('ID'+str(SymTab.randomIdGen(idlist)))

        SymTab.printer(toklist, enumlist, tokidlist, toklist.index(string)) # Print the table

def functionRecognizer(line):
    """A function that recognizes functions' headers"""
    obbeg = line.find('(')
    # We split the function header into two parts
    line1 = line[0:obbeg]                        # This is the first part - The function name
    line2 = line[obbeg+1:line.find(')')]         # This is the second part - The parameter list
    
    tokens =[]
    beforeob = line1.split()
    # Parameter lists are usually separated by a comma and a space or just a comma.
    # Because of this inconsistency, we handle the arglist in two parts
    afterob = line2.split()                  # A list of parameters split on the basis of whitespace
    params = []
    paramlist = []
    for parameter in afterob:
        paramindex = parameter.find(',')
        if not paramindex == -1:
            paramlist = parameter.split(',')
        else:                                # case of a single parameter
            paramlist = [parameter]
        for arg in paramlist:
            params.append(arg)
    # Add function name to list of tokens
    for lexeme in beforeob:
        tokens.append(lexeme)
    # Add name of each parameter to the list of tokens
    for lexeme in params:
        tokens.append(lexeme)

    return tokens


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
            print 'Token','\t\t\t','Type','\t\t\t\t\t','Token ID'
            for x in xrange(0, 50):
                print '-',
            print
            while True:
                line = source.readline()         # Read a line from the ruby source file
                if not line: break
                # print 'ln', ln, ':', line,      # print the line
                ln += 1                          # Increment line number count
                commbeg = line.find('#')         # Beginning of a comment
                if not commbeg == -1:
                    line = line[0:commbeg]       # Strip out the comment

                if not line.find('(') == -1:
                    tokens = functionRecognizer(line)
                
                else:
                    tokens = line.split()            # [HOWTO] This splits only on the basis of whitespace characters. Need to remove brackets too
                # for string in tokens:
                #     for symbol in SymTab.punctlist:
                #         if string.find(symbol) != -1: # [HOWTO] Now we know that the string has a symbol. Need to split the string and insert into the list again
                #             
                for token in tokens:
                    lists = [SymTab.toklist, SymTab.enumlist, SymTab.tokidlist, SymTab.kwlist, SymTab.oplist, SymTab.punctlist, SymTab.constlist, SymTab.tokidlist, SymTab.idlist]
                    SymTab.classify(lists, token)       # Analyzes the tokens
                
            source.close()
    
        else:                                    # If the extension is not '.rb'
            print sourcefile, "is not a valid ruby source"

if __name__ == '__main__':
    main()