program ::= "int" "main" "(" ")" "{" statements "}"
statements ::= { statement }
statement ::= declaration | assignment | if_statement | while_statement | printf_statement | return_statement | scanf_statement  <!-- Thêm scanf_statement -->
declaration ::= type identifier [ "=" (number | string_literal) ] ";"  <!-- Chỉ cho phép gán giá trị số/chuỗi -->
type ::= "int" | "string"
assignment ::= identifier "=" (expression | scanf_call) ";"  <!-- Cho phép gán từ biểu thức hoặc scanf -->
if_statement ::= "if" "(" condition ")" "{" statements "}"
while_statement ::= "while" "(" condition ")" "{" statements "}"
condition ::= expression comparison_op expression
comparison_op ::= ">" | "<" | "==" | "!=" | ">=" | "<="
printf_statement ::= "printf" "(" string_literal [ "," expression { "," expression } ] ")" ";"
return_statement ::= "return" expression ";"
scanf_statement ::= "scanf" "(" string_literal "," ("&" identifier | identifier) ")" ";" 
expression ::= term { ("+" | "-") term }
term ::= factor { ("*" | "/") factor }
factor ::= number | identifier | "(" expression ")"