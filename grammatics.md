# Грамматика языка

<program> ::= <terminals_set><nonterminals_set><set_of_rules>

<terminals_set> ::= T = <grammar_symbol_set>;

<nonterminals_set> ::= N = <grammar_symbol_set>;

<grammar_symbols_set> ::= '{' {<grammar_symbol>,}<grammar_symbol> '}'

<set_of_rules> ::= {<rule>;}<rule>.

<rule> ::= <non_empty_string><transforms_to><string>

<transforms_to> ::= "\->"

<string> ::= <non_empty_string> | <empty_string>

<non_empty_string> ::= {<grammar_symbol>}<grammar_symbol>

<grammar_symbol> ::= <special_letter> | <maybe_indexed_symbol

<maybe_indexed_symbol> ::= <regular_letter>(<lower_index>)(<apostrophe>)

<apostrophe> ::= '

<lower_index> ::= '_''{'<index_string>'}'

<index_string> ::= {<regular_letter>}<regular_letter>

<letter> ::= <regular_letter> | <special_letter>

<regular_letter> ::= ASCII без whitespace символов, ':', ';', '.', ',', '\', '>', '_', '{', '}', <apostrophe>

<special_letter> ::= \E - символ пустой строки,
                     \S - начальный символ,
                     \! - символ конца входных данных
                     \\

<empty_string> ::= \E 
