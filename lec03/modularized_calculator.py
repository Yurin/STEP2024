def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def read_left_paren(line, index):
    token = {'type': 'LPAREN'}
    return token, index + 1

def read_right_paren(line, index):
    token = {'type': 'RPAREN'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            (token, index) = read_left_paren(line, index)
        elif line[index] == ')':
            (token, index) = read_right_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def pop_operator(operators, token, priority):# 優先順位の高い演算子は、同じ優先順位かそれよりも高い優先順位の演算子に出会うまでスタックに留まる
    return (operators and operators[-1]['type'] in priority #スタックに演算子があるかの確認
            and 
            priority[operators[-1]['type']] >= priority[token['type']])#現在の演算子とスタック上の演算子の優先順位を比較 

def rpn_algo(tokens):#逆ポーランド記法に変換する
    priority = {'PLUS': 1, 'MINUS': 1, 'TIMES': 2, 'DIV': 2}
    output = []
    operators = []

    for token in tokens:
        if token['type'] == 'NUMBER':
            output.append(token)
        elif token['type'] == 'LPAREN':
            operators.append(token)
        elif token['type'] == 'RPAREN':
            while operators and operators[-1]['type'] != 'LPAREN':
                output.append(operators.pop())
            operators.pop()  # Remove '('
        elif token['type'] in priority:
            while pop_operator(operators, token, priority):
                output.append(operators.pop())
            operators.append(token)
    
    while operators:
        output.append(operators.pop())

    return output

def evaluate_rpn(tokens):#スタックを使用して逆ポーランド記法の式を計算する
    stack = []
    for token in tokens:
        if token['type'] == 'NUMBER':
            stack.append(token['number'])
        else:
            b = stack.pop()
            a = stack.pop()
            if token['type'] == 'PLUS':
                stack.append(a + b)
            elif token['type'] == 'MINUS':
                stack.append(a - b)
            elif token['type'] == 'TIMES':
                stack.append(a * b)
            elif token['type'] == 'DIV':
                stack.append(a / b)
    return stack[0]

def test(line):
    tokens = tokenize(line)
    rpn = rpn_algo(tokens)
    actual_answer = evaluate_rpn(rpn)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2.1*3")
    test("1+2.0*3/2")
    test("3*2+1")
    test("3+2*2")
    test("10/2-3")
    test("10-2/2")
    test("789-123")
    test("100*3")
    test("(1+2)*3")
    test("2*(3+4)")
    test("2+3*(4-1)")
    test("(2+3)*(4-1)")
    test("10/(2+3)")
    test("(10-2)/2")
    test("3*(2+1)")
    test("(3+2)*2")
    test("(10/2)-3")
    test("10-(2/2)")
    test("100/(5*2)")
    test("50-(5*3)")
    test("2*(3+4)-5")
    test("(2+3)*(4-1)+1")
    test("5/(2+3)*4")
    test("2*(3-(1+1))")
    test("(6+2)/(2*2)")
    test("8-2*(3-1)")
    test("10-(2+3)/5")
    test("3*(4/2)-1")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    rpn = rpn_algo(tokens)
    answer = evaluate_rpn(rpn)
    print("answer = %f\n" % answer)
