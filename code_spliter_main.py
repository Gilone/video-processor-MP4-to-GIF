from LineSpliter import run_code_line_spliter
from BlockSpliter import run_code_block_spliter
from ProfileJsonReader import parse_scalene_profile_json
from InputReader import read_profile_config

if __name__ == "__main__":
    profile_config_dict = parse_scalene_profile_json('./profile.json', 20, 2)
    # print(profile_config_dict)
    file_name_line_map = read_profile_config(profile_config_dict)
    run_code_line_spliter(file_name_line_map)
    run_code_block_spliter(file_name_line_map)
