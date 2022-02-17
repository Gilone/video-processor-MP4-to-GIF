from input import read_config
from mp4_converter import handler

if __name__ == '__main__':
    config_dict = read_config('config.json')
    handler(config_dict)