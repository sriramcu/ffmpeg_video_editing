#!/home/sriram/work/venv/bin/python
import os
import sys
import time

from moviepy.editor import VideoFileClip

def segment_reverser(cut_out_segments):

    clip = VideoFileClip(sys.argv[1])
    video_duration = int(clip.duration) + 1


    correctness_checker = []
    for seg in cut_out_segments:
        correctness_checker.append(seg[0])
        correctness_checker.append(seg[1])
        
    if sorted(correctness_checker)!=correctness_checker or correctness_checker[-1]>video_duration or len(correctness_checker)!=len(set(correctness_checker)):
        print("Improper cut out segments")
        sys.exit(-1)
        
    reversed_segments = []
    position = 0
    if cut_out_segments[0][0] == 0:
        position = cut_out_segments[0][1]
        del cut_out_segments[0]
    for i in range(len(cut_out_segments)):
        
        if position!=cut_out_segments[i][0]:
            reversed_segments.append([position,cut_out_segments[i][0]])
        if (i+1)<len(cut_out_segments):
            reversed_segments.append([cut_out_segments[i][1],cut_out_segments[i+1][0]])
        else:
            reversed_segments.append([cut_out_segments[i][1],video_duration])
        
        position = reversed_segments[-1][-1]

    return reversed_segments
    
    
def main():
    if(len(sys.argv))<3:
        print(f"Usage: python3 {__file__} input_file 10-45(remove this segment)")
        sys.exit(-1)
        
        
    debugger_file = open('debugger_file.txt','w')
    
    input_video_file = f'"{sys.argv[1]}"'
    
    full_ffmpeg_command = f'ffmpeg -i {input_video_file}'
    
             
    input_video_extension = input_video_file.split('.')[-1][:-1]
    final_output_file = f"final_output.{input_video_extension}"
    segments = []
    segment = list(map(int,sys.argv[2].split('-')))
    segments.append(segment)


    for i in range(3,len(sys.argv)):
        segment = list(map(int,sys.argv[i].split('-')))
        segments.append(segment)

        
    reversed_segments = segment_reverser(segments)
    # debugger_file.write(str(reversed_segments))
    
    
    interim_videos_text_file = 'interim_output_videos.txt'
    files = open(interim_videos_text_file, 'w')
    ctr = 1
    interim_files_list = []
    for segment in reversed_segments:
        segment_removal_sub_command = f' -ss {segment[0]} -to {segment[1]} interim_output{ctr}.{input_video_extension}'
        full_ffmpeg_command = full_ffmpeg_command + segment_removal_sub_command
        
        interim_file_name = f"interim_output{ctr}.{input_video_extension}"
        files.write(f"file '{interim_file_name}'\n")
        interim_files_list.append(interim_file_name)
        ctr += 1


    files.close()

    debugger_file.write(full_ffmpeg_command)
    debugger_file.close()

    os.system(full_ffmpeg_command)
    # time.sleep(5)
    
    os.system(f"ffmpeg -f concat -i {interim_videos_text_file} -c copy {final_output_file}")

    for interim_video_file in interim_files_list:
        os.remove(interim_video_file)

    
    os.remove(interim_videos_text_file)


if __name__=='__main__':
    main()
    

