import json, os
from read_profile_json import parse_scalene_profile_json

def read_config(config_dict):
    file_name_line_map = {}
    for file_path, lline_info_dict_list in config_dict.items(): # {"file_1.py":[1,2,3,5], "file_2.py":[25, 36]}
        file_path = os.path.abspath(file_path)
        line_list = []
        for line_info_dict in lline_info_dict_list:
            line_list.append(int(line_info_dict['line']-1)) # line start from 1, while list start from 0
        file_name_line_map[file_path] = line_list
    return file_name_line_map

# ok = frame_one.save(video_absolute_path[:-4]+".gif", format="GIF", append_images=frames,
#             save_all=True, duration=50, loop=0)   take this as the example
def generate_func(code_string, function_name):
    leading_space = (len(code_string) - len(code_string.lstrip())) * ' '

    code_string = code_string.replace(' ', '').strip().split('#')[0]
    if '=' in code_string and '(' not in code_string.split('=')[0]:
        return_string = code_string.split('=')[0] # ok
        func_call_string = code_string.split('=')[1]  # frame_one.save(video_absolute_path[:-4]+".gif", format="GIF", append_images=frames,save_all=True, duration=50, loop=0)
    else:
        return_string = ''
        func_call_string = code_string

    method_string = func_call_string.split('(')[0].split('.')[0]  # frame_one

    other_param_list = func_call_string.split('(')[1].split(')')[-2].split(',') # [video_absolute_path[:-4]+".gif", format="GIF", append_images=frames,save_all=True, duration=50, loop=0]
    other_param_string = []
    for other_param in other_param_list:
        if not other_param:
            continue
        if '=' in other_param:
            other_param = other_param.split('=')[1]
        if '+' in other_param:
            other_param = other_param.split('+') # [video_absolute_path[:-4], ".gif"]
        else:
            other_param = [other_param]
        for param in other_param:
            if param[0] != '\"' and not param.isdigit() and param != 'True' and param != 'False':
                if '[' in param:
                    other_param_string.append(param.split('[')[0])  # video_absolute_path
                else:
                    other_param_string.append(param)

    if other_param_string:
        other_param_string = ',' + (',').join(other_param_string)
    else:
        other_param_string = ''

    FUNC_BODY_TEMPLATE = \
    '''
def {func_name}({param}):
    {func_body}
    return {return_string}
    '''

    FUNC_CALL_TEMPLATE = "{func_name}({param})\n"

    function_body = FUNC_BODY_TEMPLATE.format(func_name=function_name, param=method_string+other_param_string ,func_body=code_string, return_string=return_string)
    function_call = FUNC_CALL_TEMPLATE.format(func_name=function_name, param=method_string+other_param_string)
    if return_string:
        function_call = leading_space + return_string + " = " + function_call
    else:
        function_call = leading_space + function_call
    return function_call, function_body

def modify_script(script_list, line_list):
    line_list.sort()    
    for line in line_list:
        code_string = script_list[line]
        function_call, function_body = generate_func(code_string, 'new_func_line_'+str(line))
        script_list[line] = function_call
        script_list.append(function_body)

def run():
    config_dict = parse_scalene_profile_json('./profile.json', 20, 2)
    file_name_line_map = read_config(config_dict)
    for file_path, line_list in file_name_line_map.items():
        script_list = []
        # line_list = [28, 61] # for test
        with open(file_path, 'r') as script_file:
            script_list = script_file.readlines()
            modify_script(script_list, line_list)
        with open(file_path[:-3]+'_modified.py', 'w') as script_file:
            script_file.writelines(script_list)
    

if __name__ == "__main__":
    run()