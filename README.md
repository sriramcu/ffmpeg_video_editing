# FFMPEG cut multiple segments simultaneously
Easy and convenient way of cutting videos using ffmpeg.  
Cut multiple segments off any video with just one command.

## Setup

1. Install FFMPEG
2. `pip install -r requirements.txt`

## Usage  

`python3 ffmpeg_batch_cut.py -i <input_file> -ss 10-45 100-125 (remove these segments)`

**OR**

`python3 ffmpeg_batch_cut.py -i <input_file> -s 00:10-00:45 01:40-02:05 (remove these 
segments)`
