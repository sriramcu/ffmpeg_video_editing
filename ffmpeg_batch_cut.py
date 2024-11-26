import argparse
import os
import time

from moviepy.editor import VideoFileClip

import utils


def check_segment_correctness(to_be_removed_segments: list[list[int]], video_duration):
    correctness_checker = []
    for seg in to_be_removed_segments:
        correctness_checker.append(seg[0])
        correctness_checker.append(seg[1])

    if sorted(correctness_checker) != correctness_checker or correctness_checker[-1] > video_duration or len(
            correctness_checker) != len(set(correctness_checker)):
        # Checks if the segments are in the correct order, the highest segment is less than the duration of the video,
        # and that there are no duplicates
        raise ValueError("Improper removal segments " + str(to_be_removed_segments))


def segment_reverser(to_be_removed_segments, video_duration):
    """
    Converts segments to be removed from the video to segments of the video to be preserved
    """
    reversed_segments = []
    position = 0
    if to_be_removed_segments and to_be_removed_segments[0][0] == 0:
        position = to_be_removed_segments[0][1]
        to_be_removed_segments = to_be_removed_segments[1:]
    for i in range(len(to_be_removed_segments)):

        if position != to_be_removed_segments[i][0]:
            reversed_segments.append([position, to_be_removed_segments[i][0]])
        if (i + 1) < len(to_be_removed_segments):
            reversed_segments.append([to_be_removed_segments[i][1], to_be_removed_segments[i + 1][0]])
        else:
            reversed_segments.append([to_be_removed_segments[i][1], video_duration])
        position = reversed_segments[-1][-1]

    if not reversed_segments:
        reversed_segments.append([position, video_duration])
    return reversed_segments


def ffmpeg_batch_cut(segments: list[list[int]], input_file_path, output_file_path):
    input_file_path = os.path.abspath(input_file_path)
    debugger_folder_path = os.path.join(os.path.dirname(input_file_path), "generated_text_files")
    os.makedirs(debugger_folder_path, exist_ok=True)
    debugger_file_path = os.path.join(debugger_folder_path, "debugger_file.txt")
    debugger_file = open(debugger_file_path, 'w')
    full_ffmpeg_command = f'ffmpeg -i "{input_file_path}" -c copy'
    # initial variable that will be appended to during the for loop iterating over the reversed segments

    input_video_extension = input_file_path.split('.')[-1].strip()  # without the '.'
    if not output_file_path:
        output_file_path = f"final_output.{input_video_extension}"

    output_file_path = os.path.abspath(output_file_path)
    clip = VideoFileClip(input_file_path)
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

    concat_command = f'ffmpeg -f concat -i {interim_videos_text_file} -c copy "{output_file_path}"'
    os.system(concat_command)
    for interim_video_file in interim_files_list:
        os.remove(interim_video_file)
    os.remove(interim_videos_text_file)


def main():
    parser = argparse.ArgumentParser(description='Remove segments from a video file')
    parser.add_argument('-i', '--input_file', type=str, help='Input video file', required=True)
    parser.add_argument('-s', '--segments', type=str, nargs='+', help='Segments to remove in the format \"0:10-1:05\"',
                        required=False)
    parser.add_argument('-ss', '--segments_seconds', type=str, nargs='+',
                        help='Segments to remove in the format \"10-65\"', required=False)
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
