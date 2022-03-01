import cv2
import os
import glob
import shutil
from PIL import Image
# from memory_profiler import profile
from scalene import scalene_profiler, profile

# split one original video into multiple small slices
@profile
def split_video(video_absolute_path):
    video_capture = cv2.VideoCapture(video_absolute_path)
    
    original_video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    original_video_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    original_video_frame_number = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print('[Info] Original video info: fps {}  size {} nums {}'.format(original_video_fps, original_video_size, original_video_frame_number))

    cur_video_number = 0
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    cur_video_writer = cv2.VideoWriter(video_absolute_path[:-4]+"_"+str(cur_video_number)+".mp4", fourcc, original_video_fps, original_video_size)

    frame_counter = -1
    sec_per_video = 10  # 10 second per video slice
    frame_number_of_each_slice = sec_per_video * original_video_fps # frame number of each second

    while video_capture.isOpened():
        frame_counter += 1
        success, frame = video_capture.read() # split
        if success:
            if (frame_counter % frame_number_of_each_slice < frame_number_of_each_slice - 1):
                cur_video_writer.write(frame) # append frame in to current video slice # split
            else:
                cur_video_number += 1
                cur_video_writer = cv2.VideoWriter(video_absolute_path[:-4]+"_"+str(cur_video_number)+".mp4", fourcc, original_video_fps, original_video_size) # start to write another video slice
        else:
            break
    print("[Info] Splited", cur_video_number, "videos")
    video_capture.release()
    return cur_video_number

@profile
def convert_mp4_to_jpgs(cur_video_absolute_path, video_frames_folder_absolute_path, key_frame_step):
    original_video_name = os.path.basename(cur_video_absolute_path)
    video_capture = cv2.VideoCapture(cur_video_absolute_path)
    still_reading, frame = video_capture.read() # split
    frame_counter = 0
    f, video_capture, still_reading, jpg, _, frame, key_frame_step, original_video_name, frame_counter, video_frames_folder_absolute_path = new_func_block_47(f, video_capture, still_reading, jpg, _, frame, key_frame_step, original_video_name, frame_counter, video_frames_folder_absolute_path)




    print("[Info] Read", frame_counter//key_frame_step, "frames from ", cur_video_absolute_path)

@profile
def convert_jpgs_to_gif(video_frames_folder_absolute_path, video_absolute_path):
    images = glob.glob(f"{video_frames_folder_absolute_path}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    if frames:
        frame_one = frames[0]
        frame_one.save(video_absolute_path[:-4]+".gif", format="GIF", append_images=frames, save_all=True, duration=50, loop=0) # split
    print("[Info] Converte finished", video_absolute_path)

@profile
def clean_frame_folder(video_frames_folder_absolute_path):
    if os.path.exists(video_frames_folder_absolute_path):
        shutil.rmtree(video_frames_folder_absolute_path) # delete previous results
    try:
        os.mkdir(video_frames_folder_absolute_path)
    except IOError:
        print("[Error] Can not create output folder")
        os.exit(0)

def run_converter(config):
    scalene_profiler.start()
    key_frame_step = 100 # get one key frame pre 100 frames
    video_path_list = config.get('video_file_list')
    video_base_dir = config.get('video_dir')
    video_frames_folder_name = config.get('video_frames_folder_name')
    video_frames_folder_absolute_path = os.path.abspath(os.path.join(video_base_dir, video_frames_folder_name))

    clean_frame_folder(video_frames_folder_absolute_path)
    # could covert multiple video
    for video_absolute_path in video_path_list:
        splited_video_number = split_video(video_absolute_path)
        for video_number in range(0, splited_video_number+1):
            cur_video_absolute_path = video_absolute_path[:-4] + "_"+str(video_number)+".mp4"
            convert_mp4_to_jpgs(cur_video_absolute_path, video_frames_folder_absolute_path, key_frame_step)

        convert_jpgs_to_gif(video_frames_folder_absolute_path, video_absolute_path)
    print("[Info] Finished")
    scalene_profiler.stop()

def new_func_block_47(f, video_capture, still_reading, jpg, _, frame, key_frame_step, original_video_name, frame_counter, video_frames_folder_absolute_path):
    while still_reading:
        if frame_counter % key_frame_step == 0:
            cv2.imwrite(f"{video_frames_folder_absolute_path}/{original_video_name}_{frame_counter}.jpg", frame)
        still_reading, frame = video_capture.read() 
        frame_counter += 1

    return f, video_capture, still_reading, jpg, _, frame, key_frame_step, original_video_name, frame_counter, video_frames_folder_absolute_path
