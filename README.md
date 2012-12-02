RubyLexer
=========

A lexical analyzer for Ruby in Python

Usage
=====

python rubylexer.py -s/--source __list_of_ruby_source_files__

- Takes a ruby source file as input
- Prints the Symbol Table on the standard output

Example
=======

__ruby.rb__
`print "Hello World!"`

__$__python rubylexer.py -s ruby.rb

Ruby source file: ruby.rb
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
Token                   Type                                    Token ID
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
'Hello World!'          string literal                          CT1163
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print                   identifier                              ID557
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -