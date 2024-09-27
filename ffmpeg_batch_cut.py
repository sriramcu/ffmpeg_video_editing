import argparse
import os
import time

from moviepy.editor import VideoFileClip

import utils


def check_segment_correctness(cut_out_segments, video_duration):
    correctness_checker = []
    for seg in cut_out_segments:
        correctness_checker.append(seg[0])
        correctness_checker.append(seg[1])

    if sorted(correctness_checker) != correctness_checker or correctness_checker[-1] > video_duration or len(
            correctness_checker) != len(set(correctness_checker)):
        # Checks if the segments are in the correct order, the highest segment is less than the duration of the video,
        # and that there are no duplicates
        raise ValueError("Improper cut out segments")


def segment_reverser(cut_out_segments, video_duration):
    """
    Converts segments cut out from the video to segments of the video to be preserved
    """
    reversed_segments = []
    position = 0
    if cut_out_segments[0][0] == 0:
        position = cut_out_segments[0][1]
        del cut_out_segments[0]
    for i in range(len(cut_out_segments)):

        if position != cut_out_segments[i][0]:
            reversed_segments.append([position, cut_out_segments[i][0]])
        if (i + 1) < len(cut_out_segments):
            reversed_segments.append([cut_out_segments[i][1], cut_out_segments[i + 1][0]])
        else:
            reversed_segments.append([cut_out_segments[i][1], video_duration])
        position = reversed_segments[-1][-1]
    return reversed_segments


def ffmpeg_batch_cut(segments, args_input_file, args_output_file):
    debugger_file_name = os.path.join("generated_text_files", "debugger_file.txt")
    debugger_file = open(debugger_file_name, 'w')
    input_video_file = f'"{args_input_file}"'  # encloses input file in double quotes
    full_ffmpeg_command = f'ffmpeg -i {input_video_file} -c copy'
    # initial variable that will be appended to during the for loop iterating over the reversed segments

    input_video_extension = input_video_file.split('.')[-1][:-1]  # without the '.'
    if not args_output_file:
        final_output_file = f"final_output.{input_video_extension}"
    else:
        final_output_file = args_output_file

    clip = VideoFileClip(args_input_file)
    video_duration = int(clip.duration) + 1
    check_segment_correctness(segments, video_duration)
    segments = segment_reverser(segments, video_duration)
    debugger_file.write(str(segments))

    interim_videos_text_file = 'interim_output_videos.txt'
    files = open(interim_videos_text_file, 'w')
    ctr = 1
    interim_files_list = []
    for segment in segments:
        interim_file_name = f"interim_output{ctr}.{input_video_extension}"
        segment_extraction_sub_command = f' -ss {segment[0]} -to {segment[1]} {interim_file_name}'
        full_ffmpeg_command = full_ffmpeg_command + segment_extraction_sub_command
        files.write(f"file '{interim_file_name}'\n")
        interim_files_list.append(interim_file_name)
        ctr += 1

    files.close()

    debugger_file.write(full_ffmpeg_command)
    debugger_file.close()

    print(full_ffmpeg_command)
    os.system(full_ffmpeg_command)
    time.sleep(5)

    concat_command = f"ffmpeg -f concat -i {interim_videos_text_file} -c copy {final_output_file}"
    os.system(concat_command)
    for interim_video_file in interim_files_list:
        os.remove(interim_video_file)
    os.remove(interim_videos_text_file)


def main():
    parser = argparse.ArgumentParser(description='Cut out segments from a video file')
    parser.add_argument('-i', '--input_file', type=str, help='Input video file', required=True)
    parser.add_argument('-s', '--segments', type=str, nargs='+', help='Segments to cut out in the format \"0:10-1:05\"',
                        required=False)
    parser.add_argument('-ss', '--segments_seconds', type=str, nargs='+',
                        help='Segments to cut out in the format \"10-65\"', required=False)
    parser.add_argument('-o', '--output_file', type=str, help='Output video file location', required=False)
    args = parser.parse_args()
    flag1 = False
    flag2 = False
    segments = []
    if args.segments:
        flag1 = True
        segments = utils.time_intervals_converter(args.segments)
    if args.segments_seconds:
        flag2 = True
        segments = args.segments_seconds

    if flag1 == flag2 or segments == []:
        raise ValueError("Exactly one of -s or -ss must be specified")

    segments = [list(map(int, seg.split('-'))) for seg in segments]
    print(segments)
    ffmpeg_batch_cut(segments, args.input_file, args.output_file)


if __name__ == '__main__':
    main()
