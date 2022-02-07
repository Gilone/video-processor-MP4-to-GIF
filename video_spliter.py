import os
import subprocess
import glob

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def splite_video(args):
    ret = subprocess.run([os.path.join(SCRIPT_DIR, 'ffmpeg'), '-y'] + args,
        #subprocess might inherit Lambda's input for some reason
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if ret.returncode != 0:
        print('Invocation of ffmpeg failed!')
        print('Out: ', ret.stdout.decode('utf-8'))
        raise RuntimeError()


def handler(video_dir, video_path, time_str):
    
    # file_path = os.path.join(video_dir, os.path.basename(video_path))

    video_title = video_path.split('.mp4')[0]
    file_num = len(glob.glob(os.path.join(video_dir, '*.mp4')))
    copy_path = video_title + '_' + str(file_num) + '.mp4'

    time_list = time_str.split(' ')
    start_time = ":".join(time_list[:-1])
    duration = time_list[-1]
    print(start_time, duration)

    args = ["-ss", start_time,
    "-i", video_path,
    "-t", duration,
    "-c", "copy", copy_path]

    splite_video(args)

def run(video_list, file_id):

    # 切割一段 00 00 00 10  开始时间00 00 00    时长10
    # 切割多段 00 00 00 10,00 00 00 20,00 00 00 30
    duration_list = ["00 00 00 10", "00 00 00 20", "00 00 00 30"]

    for time_duration in duration_list:
        handler(video_list, file_id, time_duration)