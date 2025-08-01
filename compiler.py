import re,sys

TOKENS = [
    # Kiểu dữ liệu cơ bản C: int hoặc string
    ('TYPE',           r'\b(int|string)\b'),
    # Các từ khóa điều khiển IO
    ('PRINTF',         r'\bprintf\b'),
    ('SCANF',          r'\bscanf\b'),
    # Các từ khóa điều khiển luồng
    ('IF',             r'\bif\b'),
    ('ELSE',           r'\belse\b'),
    ('WHILE',          r'\bwhile\b'),
    ('RETURN',         r'\breturn\b'),
    # Ký tự đặc biệt
    ('AMPERSAND',      r'&'),
    # Tên biến, hàm: bắt đầu bằng chữ hoặc gạch dưới, tiếp theo có thể là chữ/số/gạch dưới
    ('IDENTIFIER',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
    # Số nguyên (liên tiếp các chữ số)
    ('NUMBER',         r'\d+'),
    # Xâu ký tự: mở bằng " và cho phép escape nội bộ
    ('STRING_LITERAL', r'"([^"\\]|\\.)*"'),
    # Các toán tử so sánh
    ('COMPARE_OP',     r'>=|<=|==|!=|>|<'),
    # Toán tử gán
    ('ASSIGN',         r'='),
    # Toán tử số học: + - * /
    ('ARITH_OP',       r'\+|-|\*|/'),
    # Dấu ngoặc, dấu ngoặc nhọn, chấm phẩy, phẩy
    ('LPAREN',         r'\('),
    ('RPAREN',         r'\)'),
    ('LBRACE',         r'\{'),
    ('RBRACE',         r'\}'),
    ('SEMI',           r';'),
    ('COMMA',          r','),
]

def lex(code):
    tokens = []
    while code:
        code = code.lstrip()
        if not code:
            break
        for tok_name, tok_re in TOKENS:
            match = re.match(tok_re, code)
            if match:
                value = match.group(0)
                tokens.append((tok_name, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of input")
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token[0]}")
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f"Expected {expected_value}, got {token[1]}")
        self.pos += 1
        return token

    def parse(self):
        self.consume('TYPE', 'int')
        self.consume('IDENTIFIER', 'main')
        self.consume('LPAREN')
        self.consume('RPAREN')
        self.consume('LBRACE')
        statements = self.parse_statements()
        self.consume('RBRACE')
        return {'type': 'program', 'body': statements}

    def parse_statements(self):
        statements = []
        while self.peek() and self.peek()[0] != 'RBRACE':
            next_tok = self.peek()[0]
            if next_tok == 'TYPE':
                statements.append(self.parse_declaration())  # Handle declarations
            elif next_tok == 'IDENTIFIER':
                statements.append(self.parse_assignment())  # Handle assignments
            elif next_tok == 'PRINTF':
                statements.append(self.parse_printf_statement())  # Handle printf statement
            elif next_tok == 'SCANF':
                statements.append(self.parse_scanf_statement())  # Handle scanf statement
            elif next_tok == 'IF':
                statements.append(self.parse_if_statement())  # Handle if statement
            elif next_tok == 'WHILE':
                statements.append(self.parse_while_statement())  # Handle while statement
            elif next_tok == 'RETURN':
                statements.append(self.parse_return_statement())  # Handle return statement
            else:
                raise SyntaxError(f"Unexpected token: {self.peek()}")
        return statements

    def parse_declaration(self):
        var_type = self.consume('TYPE')[1]  # Consume the type (e.g., int, string)
        var_name = self.consume('IDENTIFIER')[1]  # Consume the variable name
        initial_value = None  # Default to no initial value
        
        # Check for assignment (initialization)
        if self.peek() and self.peek()[0] == 'ASSIGN':
            self.consume('ASSIGN')  # Consume the assignment operator
            initial_value = self.parse_expression()  # Parse the entire expression
        
        self.consume('SEMI')  # Consume the semicolon marking the end of the declaration
        
        # Return the declaration node
        return {'type': 'declaration', 'var_type': var_type, 'var_name': var_name, 'initial_value': initial_value}
    
    def parse_assignment(self):
        var_name = self.consume('IDENTIFIER')[1]
        self.consume('ASSIGN')
        if self.peek()[0] == 'SCANF':
            rhs = self.parse_scanf_call()
        else:
            rhs = self.parse_expression()
        self.consume('SEMI')
        return {'type': 'assignment', 'var_name': var_name, 'rhs': rhs}

    def parse_scanf_call(self):
        self.consume('SCANF')
        self.consume('LPAREN')
        format_str = self.consume('STRING_LITERAL')[1]
        self.consume('COMMA')
        if self.peek()[0] == 'AMPERSAND':
            self.consume('AMPERSAND')
            var_name = self.consume('IDENTIFIER')[1]
            is_address = True
        else:
            var_name = self.consume('IDENTIFIER')[1]
            is_address = False
        self.consume('RPAREN')
        return {'type': 'scanf_call', 'format': format_str, 'var_name': var_name, 'is_address': is_address}

    def parse_printf_statement(self):
        self.consume('PRINTF')
        self.consume('LPAREN')
        format_str = self.consume('STRING_LITERAL')[1]
        args = []
        while self.peek() and self.peek()[0] == 'COMMA':
            self.consume('COMMA')
            args.append(self.parse_expression())
        self.consume('RPAREN')
        self.consume('SEMI')
        return {'type': 'printf_statement', 'format': format_str, 'args': args}

    def parse_scanf_statement(self):
        self.consume('SCANF')
        self.consume('LPAREN')
        format_str = self.consume('STRING_LITERAL')[1]
        self.consume('COMMA')
        if self.peek()[0] == 'AMPERSAND':
            self.consume('AMPERSAND')
            var_name = self.consume('IDENTIFIER')[1]
            is_address = True
        else:
            var_name = self.consume('IDENTIFIER')[1]
            is_address = False
        self.consume('RPAREN')
        self.consume('SEMI')
        return {'type': 'scanf_statement', 'format': format_str, 'var_name': var_name, 'is_address': is_address}
    def parse_if_statement(self):
        self.consume('IF')  # Tiêu thụ từ khóa "if"
        self.consume('LPAREN')  # Tiêu thụ dấu "("
        condition = self.parse_condition()  # Phân tích điều kiện
        self.consume('RPAREN')  # Tiêu thụ dấu ")"
        self.consume('LBRACE')  # Tiêu thụ dấu "{"
        if_body = self.parse_statements()  # Phân tích các câu lệnh trong thân if
        self.consume('RBRACE')  # Tiêu thụ dấu "}"
        else_body = []  # Mặc định thân else là rỗng
        if self.peek() and self.peek()[0] == 'ELSE':  # Kiểm tra nếu có else
            self.consume('ELSE')  # Tiêu thụ từ khóa "else"
            self.consume('LBRACE')  # Tiêu thụ dấu "{"
            else_body = self.parse_statements()  # Phân tích thân else
            self.consume('RBRACE')  # Tiêu thụ dấu "}"
        return {
            'type': 'if_statement',
            'condition': condition,
            'if_body': if_body,
            'else_body': else_body
        }

    def parse_while_statement(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        condition = self.parse_condition()
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = self.parse_statements()
        self.consume('RBRACE')
        return {'type': 'while_statement', 'condition': condition, 'body': body}

    def parse_return_statement(self):
        self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return {'type': 'return_statement', 'expr': expr}

    def parse_condition(self):
        left = self.parse_expression()
        op = self.consume('COMPARE_OP')[1]
        right = self.parse_expression()
        return {'type': 'condition', 'left': left, 'op': op, 'right': right}

    def parse_expression(self):
        node = self.parse_term()
        while self.peek() and self.peek()[0] == 'ARITH_OP' and self.peek()[1] in ('+', '-'):
            op = self.consume('ARITH_OP')[1]
            right = self.parse_term()
            node = {'type': 'binary_op', 'op': op, 'left': node, 'right': right}
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek()[0] == 'ARITH_OP' and self.peek()[1] in ('*', '/'):
            op = self.consume('ARITH_OP')[1]
            right = self.parse_factor()
            node = {'type': 'binary_op', 'op': op, 'left': node, 'right': right}
        return node

    def parse_factor(self):
        token = self.peek()  # Xem token tiếp theo mà không tiêu thụ nó
        if token[0] == 'LPAREN':  # Xử lý biểu thức trong ngoặc
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        elif token[0] == 'NUMBER':  # Xử lý số
            value = self.consume('NUMBER')[1]
            return {'type': 'number', 'value': value}
        elif token[0] == 'STRING_LITERAL':  # Thêm xử lý cho chuỗi
            value = self.consume('STRING_LITERAL')[1]
            return {'type': 'string_literal', 'value': value}
        elif token[0] == 'IDENTIFIER':  # Xử lý tên biến
            name = self.consume('IDENTIFIER')[1]
            return {'type': 'identifier', 'name': name}
        else:
            raise SyntaxError(f"Unexpected token: {token}")

class SemanticAnalyzer:
    def __init__(self, ast):
        self.symbol_table = {}
        self.ast = ast

    def check(self):
        self.visit_node(self.ast)

    def visit_node(self, node):
        if node['type'] == 'program':
            for stmt in node['body']:
                self.visit_node(stmt)
        elif node['type'] == 'declaration':
            var_name = node['var_name']
            if var_name in self.symbol_table:
                raise NameError(f"Duplicate declaration: {var_name}")
            self.symbol_table[var_name] = node['var_type']
            if node['initial_value']:  # Kiểm tra nếu có giá trị khởi tạo
                self.visit_expression(node['initial_value'])
        elif node['type'] == 'assignment':
            var_name = node['var_name']
            if var_name not in self.symbol_table:
                raise NameError(f"Undeclared variable: {var_name}")
            self.visit_expression(node['rhs'])
        elif node['type'] == 'printf_statement':
            for arg in node['args']:
                self.visit_expression(arg)
        elif node['type'] == 'scanf_statement':
            var_name = node['var_name']
            if var_name not in self.symbol_table:
                raise NameError(f"Undeclared variable: {var_name}")
        elif node['type'] == 'if_statement':
            self.visit_condition(node['condition'])
            for stmt in node['if_body']:
                self.visit_node(stmt)
            for stmt in node.get('else_body', []):
                self.visit_node(stmt)
        elif node['type'] == 'while_statement':
            self.visit_condition(node['condition'])
            for stmt in node['body']:
                self.visit_node(stmt)
        elif node['type'] == 'return_statement':
            self.visit_expression(node['expr'])

    def visit_expression(self, node):
        if node['type'] == 'identifier':
            if node['name'] not in self.symbol_table:
                raise NameError(f"Undeclared variable: {node['name']}")
        elif node['type'] in ['number', 'string_literal']:
            pass  # Không cần kiểm tra thêm cho number hoặc string_literal
        elif node['type'] == 'binary_op':
            self.visit_expression(node['left'])
            self.visit_expression(node['right'])
        else:
            raise ValueError(f"Unknown expression type: {node['type']}")

    def visit_condition(self, node):
        self.visit_expression(node['left'])
        self.visit_expression(node['right'])

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.symbol_table = {}
        self.current_offset = -8
        self.stack_size = 0  # Theo dõi kích thước stack

    def generate(self, ast):
        self.emit('.section .text')
        self.emit('.globl main')
        self.emit('main:')
        self.emit('pushq %rbp')
        self.emit('movq %rsp, %rbp')
        self.allocate_variables(ast)
        for stmt in ast['body']:
            self.generate_stmt(stmt)
        self.emit('movq $0, %rax')
        self.emit('leave')
        self.emit('ret')
        return '\n'.join(self.code)

    def allocate_variables(self, ast):
        for node in ast['body']:
            if node['type'] == 'declaration':
                var_name = node['var_name']
                var_type = node['var_type']
                # Cấp phát offset cho biến
                if var_type == 'string' and not node['initial_value']:
                    # Cấp phát 256 byte cho string trên stack
                    self.stack_size += 256
                    self.symbol_table[var_name] = {'offset': self.current_offset, 'type': var_type, 'size': 256}
                    self.emit(f'subq $256, %rsp')
                    self.emit(f'movq %rsp, {self.current_offset}(%rbp)')
                else:
                    self.symbol_table[var_name] = {'offset': self.current_offset, 'type': var_type, 'size': 8}
                    self.emit(f'movl $0, {self.current_offset}(%rbp)')  # Khởi tạo mặc định
                self.current_offset -= 8

                # Xử lý initial_value
                if node['initial_value']:
                    if var_type == 'int':
                        if node['initial_value']['type'] == 'number':
                            self.emit(f'movl ${node["initial_value"]["value"]}, {self.symbol_table[var_name]["offset"]}(%rbp)')
                        elif node['initial_value']['type'] == 'binary_op':
                            left = node['initial_value']['left']
                            right = node['initial_value']['right']
                            op = node['initial_value']['op']
                            if left['type'] == 'identifier':
                                self.emit(f'movl {self.symbol_table[left["name"]]["offset"]}(%rbp), %eax')
                            elif left['type'] == 'number':
                                self.emit(f'movl ${left["value"]}, %eax')
                            if right['type'] == 'identifier':
                                self.emit(f'movl {self.symbol_table[right["name"]]["offset"]}(%rbp), %ebx')
                            elif right['type'] == 'number':
                                self.emit(f'movl ${right["value"]}, %ebx')
                            if op == '+':
                                self.emit('addl %ebx, %eax')
                            elif op == '-':
                                self.emit('subl %ebx, %eax')
                            elif op == '*':
                                self.emit('imull %ebx, %eax')
                            elif op == '/':
                                self.emit('cdq')
                                self.emit('idivl %ebx')
                            self.emit(f'movl %eax, {self.symbol_table[var_name]["offset"]}(%rbp)')
                    elif var_type == 'string':
                        label = self.new_label()
                        self.emit('.section .rodata')
                        self.emit(f'{label}: .string {node["initial_value"]["value"]}')
                        self.emit('.section .text')
                        self.emit(f'lea {label}(%rip), %rax')
                        self.emit(f'movq %rax, {self.symbol_table[var_name]["offset"]}(%rbp)')

    def generate_stmt(self, node):
        if node['type'] == 'printf_statement':
            self.generate_printf(node)
        elif node['type'] == 'scanf_statement':
            self.generate_scanf(node)
        elif node['type'] == 'assignment':
            self.generate_assignment(node)
        elif node['type'] == 'if_statement':
            self.generate_if(node)
        elif node['type'] == 'while_statement':
            self.generate_while(node)
        elif node['type'] == 'return_statement':
            self.generate_return(node)

    def generate_printf(self, node):
        fmt_label = self.new_label()
        self.emit('.section .rodata')
        self.emit(f'{fmt_label}: .string {node["format"]}')
        self.emit('.section .text')
        self.emit(f'lea {fmt_label}(%rip), %rdi')
        if node['args']:
            arg = node['args'][0]
            if arg['type'] == 'identifier':
                var_info = self.symbol_table[arg['name']]
                if var_info['type'] == 'int':
                    self.emit(f'movl {var_info["offset"]}(%rbp), %esi')
                elif var_info['type'] == 'string':
                    self.emit(f'movq {var_info["offset"]}(%rbp), %rsi')
            elif arg['type'] == 'number':
                self.emit(f'movl ${arg["value"]}, %esi')
        self.emit('mov $0, %eax')
        self.emit('call printf')

    def generate_scanf(self, node):
        fmt_label = self.new_label()
        self.emit('.section .rodata')
        self.emit(f'{fmt_label}: .string {node["format"]}')
        self.emit('.section .text')
        self.emit(f'lea {fmt_label}(%rip), %rdi')
        var_info = self.symbol_table[node['var_name']]
        if node['is_address']:
            self.emit(f'lea {var_info["offset"]}(%rbp), %rsi')
        else:
            self.emit(f'movq {var_info["offset"]}(%rbp), %rsi')
        self.emit('mov $0, %eax')
        self.emit('call scanf')

    def generate_assignment(self, node):
        var_name = node['var_name']
        var_offset = self.symbol_table[var_name]['offset']
        rhs = node['rhs']
        if rhs['type'] == 'binary_op':
            left = rhs['left']
            right = rhs['right']
            op = rhs['op']
            if left['type'] == 'identifier':
                self.emit(f'movl {self.symbol_table[left["name"]]["offset"]}(%rbp), %eax')
            elif left['type'] == 'number':
                self.emit(f'movl ${left["value"]}, %eax')
            if right['type'] == 'identifier':
                self.emit(f'movl {self.symbol_table[right["name"]]["offset"]}(%rbp), %ebx')
            elif right['type'] == 'number':
                self.emit(f'movl ${right["value"]}, %ebx')
            if op == '+':
                self.emit('addl %ebx, %eax')
            elif op == '-':
                self.emit('subl %ebx, %eax')
            elif op == '*':
                self.emit('imull %ebx, %eax')
            elif op == '/':
                self.emit('cdq')
                self.emit('idivl %ebx')
            self.emit(f'movl %eax, {var_offset}(%rbp)')

    def generate_if(self, node):
        else_label = self.new_label()
        end_label = self.new_label()
        self.generate_condition(node['condition'], else_label)
        for stmt in node['if_body']:
            self.generate_stmt(stmt)
        self.emit(f'jmp {end_label}')
        self.emit(f'{else_label}:')
        for stmt in node.get('else_body', []):
            self.generate_stmt(stmt)
        self.emit(f'{end_label}:')

    def generate_condition(self, condition, false_label):
        left = condition['left']
        right = condition['right']
        op = condition['op']
        if left['type'] == 'identifier':
            left_offset = self.symbol_table[left['name']]['offset']
            self.emit(f'movl {left_offset}(%rbp), %eax')
        elif left['type'] == 'number':
            self.emit(f'movl ${left["value"]}, %eax')
        if right['type'] == 'identifier':
            right_offset = self.symbol_table[right['name']]['offset']
            self.emit(f'cmpl {right_offset}(%rbp), %eax')
        elif right['type'] == 'number':
            self.emit(f'cmpl ${right["value"]}, %eax')
        jump_instruction = {
            '>': 'jle',
            '<': 'jge',
            '==': 'jne',
            '!=': 'je',
            '>=': 'jl',
            '<=': 'jg'
        }.get(op, 'jne')
        self.emit(f'{jump_instruction} {false_label}')

    def generate_while(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        self.emit(f'{start_label}:')
        self.generate_condition(node['condition'], end_label)
        for stmt in node['body']:
            self.generate_stmt(stmt)
        self.emit(f'jmp {start_label}')
        self.emit(f'{end_label}:')

    def generate_return(self, node):
        if node['expr']['type'] == 'number':
            self.emit(f'movq ${node["expr"]["value"]}, %rax')
        self.emit('leave')
        self.emit('ret')

    def new_label(self):
        self.label_count += 1
        return f'.L{self.label_count}'

    def emit(self, line):
        self.code.append(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 compiler.py <input.c> <output.s>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file) as f:
        code = f.read()
    
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()
    semantic = SemanticAnalyzer(ast)
    semantic.check()
    gen = CodeGenerator()
    asm_code = gen.generate(ast)
    
    with open(output_file, 'w') as f:
        f.write(asm_code + '\n')