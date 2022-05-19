#!/home/sriram/work/venv/bin/python
import os
import sys
import time

from moviepy.editor import VideoFileClip

def segment_reverser(cut_out_segments):

    clip = VideoFileClip(sys.argv[1])
    length = int(clip.duration)+1


    correctness_checker = []
    for seg in cut_out_segments:
        correctness_checker.append(seg[0])
        correctness_checker.append(seg[1])
        
    if sorted(correctness_checker)!=correctness_checker or correctness_checker[-1]>length or len(correctness_checker)!=len(set(correctness_checker)):
        print("Improper cut out segments")
        sys.exit(-1)
        
    remaining_segments = []
    position = 0
    if cut_out_segments[0][0] == 0:
        position = cut_out_segments[0][1]
        del cut_out_segments[0]
    for i in range(len(cut_out_segments)):
        
        if position!=cut_out_segments[i][0]:
            remaining_segments.append([position,cut_out_segments[i][0]])
        if (i+1)<len(cut_out_segments):
            remaining_segments.append([cut_out_segments[i][1],cut_out_segments[i+1][0]])
        else:
            remaining_segments.append([cut_out_segments[i][1],length])
        
        position = remaining_segments[-1][-1]

    return remaining_segments
    
    
def main():
    if(len(sys.argv))<3:
        print("Usage: ./ffmpeg.py input_file 10-45(remove this segment)")
        sys.exit(-1)
        
        
    debugger_file = open('debugger_file.txt','w')
    input_file = '"' + sys.argv[1] + '"'
    my_cmd = "ffmpeg -i {}".format(input_file)
    additional_segment = " -ss {} -to {} {}"    #(start,end,output file)
         
    
    ext = input_file.split('.')[-1][:-1]
    final_output_file = "final_output."+ext
    segments = []
    this_segment = list(map(int,sys.argv[2].split('-')))
    segments.append(this_segment)


    for i in range(3,len(sys.argv)):
        this_segment = list(map(int,sys.argv[i].split('-')))
        segments.append(this_segment)

        
    rem_seg = segment_reverser(segments)
    debugger_file.write(str(rem_seg))
    
    
    
    files = open('interim_output_files.txt','w')
    ctr = 1
    interim_files_list = []
    for this_segment in rem_seg:
        my_cmd = my_cmd + additional_segment.format(this_segment[0],this_segment[1]," interim_output"+str(ctr)+"."+ext)
        files.write("file 'interim_output"+str(ctr)+"."+ext+"'\n")
        interim_files_list.append("interim_output"+str(ctr)+"."+ext)
        ctr+=1


    files.close()

    debugger_file.write(my_cmd)
    os.system(my_cmd)
    time.sleep(5)
    os.system("ffmpeg -f concat -i {} -c copy {}".format("interim_output_files.txt", final_output_file))

    for ifile in interim_files_list:
        os.system("rm "+ifile)

    os.system("rm interim_output_files.txt")


if __name__=='__main__':
    main()
    

