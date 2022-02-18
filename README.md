# Video Processor for MP4-to-GIF

We want to use resource-centric style to rewrite video processing applications.

Following our main idea, in video processing applications, we can observe that the compute resource used to process frames and memory resource used to store the resources are coupled. As an example, to decode a short MP4 file, most of the memory goes to the processed memory.  

We can utilize the memory object to solve this problem. We try to directly store the output buffer into an intermediate memory object, so we can scale the memory (increase the memory obj size) and compute (allocate more compute obj on processing ) independently. Other steps (resizing, filtering) in the applications can do the same thing.

We are going to use openCV for codec, and slice the video first and process one small slice at one time. Save the output of a single slice to a memory object. Then we extract key frame from these slices and convert all frames (.jpg) to a single gif.

## Requirment

<!-- ```bash
python -m pip install ffmpy3
python -m pip install -U memory_profiler
``` -->
<!-- Download ffmpeg here: [FFMPEG build](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z),  
and then put ffmpeg.exe in the root directory. -->
```bash
python3 -m pip install opencv-python
```

## Usage

```bash
python3 run.py
```

## Ref

<!-- [serverless-benchmarks](https://github.com/spcl/serverless-benchmarks/tree/master/benchmarks/200.multimedia/220.video-processing) -->
[Blog](https://www.blog.pythonlibrary.org/2021/06/29/converting-mp4-to-animated-gifs-with-python/)