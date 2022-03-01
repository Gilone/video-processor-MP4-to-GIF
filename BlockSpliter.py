import re
from matplotlib.pyplot import sci

def parse_line(input_param_set, return_param_set, code_string, package_set):
    double_quotes_list = re.findall(r"(\"[^\"]*\")", input_str_part)
    single_quotes_list = re.findall(r"(\'[^\']*\')", input_str_part)
    key_words = [':', 'while ', 'for ', 'if ', 'in ', 'and ', 'not ', 'else ', 'str', 'int', 'range', '==', '!=', '+=', '-='] + single_quotes_list + double_quotes_list
    for key in key_words:
        code_string = code_string.replace(key, ' ')
    code_string = code_string.replace(' ', '').strip().split('#')[0]
    return_str_part = ''
    input_str_part = ''

    if '=' in code_string:
        input_str_part = code_string.split('=')[1]
        return_str_part = code_string.split('=')[0]
    else:
        input_str_part = code_string

    input_list = re.findall(r"([a-z_][\w.]*)", input_str_part)
    return_list = re.findall(r"([a-z_][\w.]*)", return_str_part)

    for input_var in input_list:
        input_var = input_var.splite('.')[0]
        if input_var in return_param_set:
            continue
        else:
            if input_var not in package_set:
                input_param_set.add(input_var)
                return_param_set.add(input_var)

    for return_var in return_list:
        return_var = return_var.splite('.')[0]
        if return_var not in package_set:
            return_param_set.add(return_var)

def modify_block(script_list, block_range, block_leading_space_len, package_set):
    function_name = 'new_func_block_'+str(block_range[0])
    BODY_FIRST_LINE_TEMPLATE = \
    '''
def {func_name}({param}):
    '''
    BODY_END_LINE_TEMPLATE = \
    '''
    return {return_string}
    '''
    FUNC_CALL_TEMPLATE = "{func_name}({param})\n"

    function_body_list = [BODY_FIRST_LINE_TEMPLATE]
    input_param_set = set()
    return_param_set = set()

    for line in range(block_range[0], block_range[1]):
        code_string = script_list[line]
        function_body_list.append(code_string[block_leading_space_len:].split('#')[0])
        parse_line(input_param_set, return_param_set, code_string, package_set)
        script_list[line] = '\n'

    if input_param_set:
        input_param_string = ', '.join(list(input_param_set))
    else:
        input_param_string = ''
    return_param_string = ', '.join(list(return_param_set))

    function_call = FUNC_CALL_TEMPLATE.format(func_name=function_name, param=input_param_string)
    if return_param_set:
        function_call = return_param_string + " = " + function_call
    script_list[block_range[0]] = block_leading_space_len * ' ' + function_call

    function_body_list.append(BODY_END_LINE_TEMPLATE)
    function_body_list[0].format(func_name=function_name, param=input_param_string)
    function_body_list[-1].format(return_string=return_param_string)
    script_list.extend(function_body_list)

def get_block_range(script_list, line):
    block_range = [line, line]
    line_start = line
    while ('def ' not in script_list[line_start]) and ('while ' not in script_list[line_start]) and ('for ' not in script_list[line_start]) and (line_start >= 0):
        line_start -= 1
    block_range[0] = line_start

    block_leading_space_len = len(script_list[line_start]) - len(script_list[line_start].lstrip())
    line_end = line
    while len(script_list[line_end]) - len(script_list[line_end].lstrip()) > block_leading_space_len and line_end<len(script_list):
        line_end += 1
    block_range[1] = line_end
    return block_leading_space_len, block_range

def get_package_set(script_list):
    package_set = set()
    for line in script_list:
        if 'import' in line:
            for l in line.splite(' '):
                if l != 'import' and l != 'from':
                    package_set.add(l)
    return package_set

def modify_script(script_list, line_list):
    package_set = get_package_set(script_list)
    line_list.sort()
    last_end = 0
    for line in line_list:
        if line < last_end:
            continue
        else:
            block_leading_space_len, block_range = get_block_range(line)
            last_end = block_range[1]
            if 'for ' in script_list[block_range[0]] or 'while ' in script_list[block_range[0]]:
                modify_block(script_list, block_range, block_leading_space_len, package_set)

def run_code_block_spliter(file_name_line_map):
    for file_path, line_list in file_name_line_map.items():
        script_list = []
        # line_list = [28, 61] # for test
        with open(file_path, 'r') as script_file:
            script_list = script_file.readlines()
            modify_script(script_list, line_list)
        with open(file_path[:-3]+'_block_modified.py', 'w') as script_file:
            script_file.writelines(script_list)