# FFMPEG cut multiple segments simultaneously
Easy and convenient way of cutting videos using ffmpeg.  
Cut multiple segments off any video with just one command.

## Setup

1. Install FFMPEG
2. `pip install -r requirements.txt`

## Usage- GUI

`python ffmpeg_batch_cut_gui.py`

Observe the demo video to see the usage:



https://github.com/user-attachments/assets/2e745be6-0d68-4289-9ba3-b10fd5acaac7



## Usage- CLI

`python ffmpeg_batch_cut.py -i <input_file> -ss 10-45 100-125 (remove these segments)`

**OR**

`python ffmpeg_batch_cut.py -i <input_file> -s 00:10-00:45 01:40-02:05 (remove these 
segments)`

Above usage (-s) supports MM:SS as well as HH:MM:SS

### Output Video

Output video will be saved in `final_output.mp4` in the current working directory, 
from where this script was run. This can be changed by using -o flag.

`python ffmpeg_batch_cut.py -i <input_file> -s 00:10-00:45 01:40-02:05 (remove these 
segments) -f path/to/output.mp4`
