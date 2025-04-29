# Грамматика языка

<program> ::= T = '{' {<symbol>,}<symbol> '}';
              N = '{' {<symbol>,}<symbol> '}';
              <set_of_rules>

<set_of_rules> ::= {<rule>;}<rule>.

<rule> ::= <non_empty_string><transforms_to><string>

<transforms_to> ::= "->"

<string> ::= <non_empty_string> | <empty_string>

<non_empty_string> ::= {<symbol>}<symbol>

<symbol> ::= <string_literal>(<lower_index>)(<upper_index>){<apostrophe>}

<lower_index> ::= <lower_index_delimeter>'{'<string_literal>'}'
<lower_index_delimeter> ::= _

<upper_index> ::= <upper_index_delimeter>'{'<string_literal>'}'
<upper_index_delimeter> ::= ^

<apostrophe> ::= '

<string_literal> ::= {<letter>}<letter>

<letter> ::= ASCII без '^', ', '=', '>', '_',
                       '', ';', 
                       '{', '}', 
                       '(', ')', 
                       '[', ']'.

<special_letter> ::= \x, где x - исключённый символ в <letter>,
                     \E - символ пустой строки,
                     \S - начальный символ.

<empty_string> ::= \E 
