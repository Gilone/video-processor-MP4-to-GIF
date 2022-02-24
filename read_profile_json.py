import json, os

'''
This function will read and parse the json output genereated by scalene and return
lines that consumes large amount of resources
'''
def parse_scalene_profile_json(json_file_path, cpu_t, memory_t):
    json_file = open(json_file_path, "r")
    profile_json = json.load(json_file)
    res = {}

    for file_name in profile_json['files']:
        line_arr = profile_json['files'][file_name]['lines']
        file_name = os.path.basename(file_name)
        # calculate usage for each line
        for line in line_arr:
            line_no = line['lineno']
            cpu_usage =  line['n_cpu_percent_c'] + line['n_cpu_percent_python'] + line['n_sys_percent']
            peak_mem = line['n_peak_mb']

            # if usage is larger than user threshold, output line number
            if cpu_usage > cpu_t or peak_mem > memory_t:
                if file_name not in res:
                    res[file_name] = []
                    
                if cpu_usage > cpu_t and peak_mem > memory_t:
                    res[file_name].append({'line' : line_no, 'category:' : 'both', 'cpu': cpu_usage, 'mem': peak_mem})
                elif cpu_usage > cpu_t:
                    res[file_name].append({'line' : line_no, 'category:' : 'cpu', 'cpu': cpu_usage, 'mem': peak_mem})
                else:
                    res[file_name].append({'line' : line_no, 'category:' : 'mem', 'cpu': cpu_usage, 'mem': peak_mem})
    
    return res

if __name__ == "__main__":
    print(parse_scalene_profile_json('./profile.json', 20, 2))
            
    