# ffmpeg_video_editing
Easy and convenient way of cutting videos using ffmpeg.  
Cut multiple segments off any video with just one command.

## Usage  

`./ffmpeg.py <input_file> 10-45 100-125 (remove these segments)`  
where segments are in seconds.  

### Helper Programs  
#### 1. Total seconds
##### Usage  
`py tot_seconds.py <time in mm:ss example 01:33 gives 93 as output>`  

#### 2. FFMPEG helper  
Uses tot_seconds.py to convert arguments which are segments in mm:ss to seconds so that they can be used in ffmpeg.py.  
##### Usage
`py ffmpeg_helper.py 10:20-11:30 11:55-32:22 ...`  
