# import datetime
# import os
# import stat
# import subprocess


# SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# def call_ffmpeg(args):
#     ret = subprocess.run([os.path.join(SCRIPT_DIR, 'ffmpeg'), '-y'] + args,
#             #subprocess might inherit Lambda's input for some reason
#             stdin=subprocess.DEVNULL,
#             stdout=subprocess.PIPE, stderr=subprocess.STDOUT
#     )
#     if ret.returncode != 0:
#         print('Invocation of ffmpeg failed!')
#         print('Out: ', ret.stdout.decode('utf-8'))
#         raise RuntimeError()

# # https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
# def to_gif(video_dir, video_path, duration):
#     output = video_dir+'/tmp/processed-{}.gif'.format(os.path.basename(video_path))
#     call_ffmpeg(["-i", video_path,
#         "-t",
#         "{0}".format(duration),
#         "-vf",
#         "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
#         "-loop", "0",
#         output])
#     return output

# def handler(config):
#     video_path_list = config.get('video_file_list')
#     duration = config.get('duration')
#     output_dir = config.get('video_dir') + '/tmp'
#     video_dir = config.get('video_dir')
#     res = []
#     # # Restore executable permission
#     # ffmpeg_binary = os.path.join(SCRIPT_DIR, 'ffmpeg')
#     # # needed on Azure but read-only filesystem on AWS
#     # try:
#     #     st = os.stat(ffmpeg_binary)
#     #     os.chmod(ffmpeg_binary, st.st_mode | stat.S_IEXEC)
#     # except OSError:
#     #     pass
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     for video_path in video_path_list:
#         process_begin = datetime.datetime.now()
#         output_path = to_gif(video_dir, video_path, duration)
#         process_end = datetime.datetime.now()

#         process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)
#         res.append({
#             'result': {
#                 'bucket': output_path,
#             },
#             'measurement': {
#                 'compute_time': process_time
#             }
#         })

#     return res