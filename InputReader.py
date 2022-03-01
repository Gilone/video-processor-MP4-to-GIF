import json, os, glob

def read_video_files_config(config_path):
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
        if not config_dict:
            print("\n[INFO]: %s is invalid." % (config_path))

    config_dict["video_file_list"] = []
    for file in glob.glob(os.path.join(config_dict['video_dir'], '*.mp4')):
        config_dict['video_file_list'].append(file)

    return config_dict


def read_profile_config(config_dict):
    file_name_line_map = {}
    for file_path, lline_info_dict_list in config_dict.items(): # {"file_1.py":[1,2,3,5], "file_2.py":[25, 36]}
        file_path = os.path.abspath(file_path)
        line_list = []
        for line_info_dict in lline_info_dict_list:
            line_list.append(int(line_info_dict['line']-1)) # line start from 1, while list start from 0
        file_name_line_map[file_path] = line_list
    return file_name_line_map