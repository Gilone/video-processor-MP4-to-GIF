import json, os, glob

def read_config(config_path):
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
        if not config_dict:
            print("\n[INFO]: %s is invalid." % (config_path))

    config_dict["video_file_list"] = []
    for file in glob.glob(os.path.join(config_dict['video_dir'], '*.mp4')):
        config_dict['video_file_list'].append(file)

    return config_dict