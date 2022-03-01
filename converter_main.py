from InputReader import read_video_files_config
from GIFConverter import run_converter

if __name__ == '__main__':
    config_dict = read_video_files_config('video_files_config.json')
    run_converter(config_dict)