# FFMPEG cut multiple segments simultaneously
Easy and convenient way of cutting videos using ffmpeg.  
Cut multiple segments off any video with just one command.

## Usage  

`python3 ffmpeg.py <input_file> 10-45 100-125 (remove these segments)`  
where segments are in seconds. The output video will be in the same directory as the input video and will be named final_output.<input_video_extension>.  

### Helper Programs  
#### 1. Total seconds
##### Usage  
`python3 tot_seconds.py <time in mm:ss example 01:33 gives 93 as output>`  

#### 2. FFMPEG helper  
Uses tot_seconds.py to convert arguments which are segments in mm:ss to seconds so that they can be used in ffmpeg.py.  
##### Usage
`python3 helper_ffmpeg.py 10:20-11:30 11:55-32:22 ...`  
  
  
### Future improvements:  
1. Add argparse to the main program and allow the user to specify the output video's name and path.
2. Argparse to other programs.