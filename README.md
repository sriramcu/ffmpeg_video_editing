# FFMPEG remove multiple segments simultaneously

Remove multiple segments from any video with just one command.  

FFMPEG command easily supports **keeping** a section of a video using the `-ss` and `-to` tags. But to do the 
reverse, i.e. **removing** certain portions of your video is a bit trickier. You need to first create a text 
file of the format:

    file video.mp4
    inpoint 34.5
    outpoint 55.1
    file video.mp4
    inpoint 111.0
    outpoint 155.3
    file video.mp4
    inpoint 278
    outpoint 316.4

Then, you need to run the command `ffmpeg -f concat -i list.txt combined.mp4`. 
[Source](https://stackoverflow.com/questions/42747935/cut-multiple-videos-and-merge-with-ffmpeg).

With my tool, you could do this in one command, without even needing to convert HH:MM:SS to seconds like in the 
text file. In this case, the one command would be:

`python ffmpeg_batch_cut.py -i video.mp4 -ss 34.5-55.1 111.0-155.3 278-316.4 combined.mp4`

OR (same timestamps in MM:SS)

`python ffmpeg_batch_cut.py -i video.mp4 -s 0:34-0:55 1:51-2:35 4:38-5:16 combined.mp4`

(These -s and -ss flags are not to be confused with those of the FFMPEG command)


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

### Command Flags

#### Required Arguments
* -i, --input_file: Input video file path (required)
#### Optional Arguments
* -s, --segments: Segments to remove in the format "0:10-1:05" (HH:MM-SS), space-separated (optional)
* -ss, --segments_seconds: Segments to remove in the format "10-65" (seconds) space-separated (optional)
* -o, --output_file: Output video file location (optional)

By default, the output video will be saved as `final_output.mp4` in the current working directory, i.e. 
from where this script was run. This can be changed by using thr `-o` flag.

`python ffmpeg_batch_cut.py -i <input_file> -s 00:10-00:45 01:40-02:05 (remove these 
segments) -f path/to/output.mp4`

## Note

This program is very fast, and can operate on a 10 minute video within 30 seconds, depending on your system. 
This is because there is no re-encoding with this technique. However, due to this very reason, you may 
experience a loss in keyframes and/or choppy videos, depending on the encoding and format of your original file.
You could try re-encoding the output to make it smooth, while saving time on re-encoding undesired segments removed 
by this tool. Do not use this tool if you need to trim in a precise manner, i.e. down to the last 
millisecond. I would recommend you to **check the final output before deleting the original**. 

The StackOverflow answers and comments on 
[this link](https://stackoverflow.com/questions/18444194/cutting-multimedia-files-based-on-start-and-end-time-using-ffmpeg) 
provide an interesting technical insight into this. [This SO post](https://stackoverflow.com/questions/50594412/cut-multiple-parts-of-a-video-with-ffmpeg)
 provides an alternative, more complex way to cut multiple parts of a video for such cases.

