import argparse
import os
import shutil
import random
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip


def is_video(file):
    print(f"Entering is_video function to check if {file} is a video file.")
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
    ext = os.path.splitext(file)[1]
    return ext.lower() in video_extensions

def find_videos(directory):
    print(f"Entering find_videos function to recursively find all video files in {directory}.")
    videos = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if is_video(filename):
                videos.append(os.path.join(dirpath, filename))
    return videos

def get_video_creation_date(video_path):
    try:
        print(f"Entering get_video_creation_date function to get creation date for {video_path}.")
        cmd = f"ffprobe -v quiet -show_entries stream_tags=creation_time -of default=noprint_wrappers=1:nokey=1 {video_path}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            print(f"Error getting creation date for {video_path}: {error}")
            return None
        else:
            creation_times = output.decode('utf-8').strip().split('\n')
            creation_times = [datetime.fromisoformat(ct) for ct in creation_times if ct]

            if not creation_times:
                print(f"No valid creation times found for {video_path}.")
                return None

            min_creation_time = min(creation_times)
            return min_creation_time
    except Exception as e:
        print(f"An error occurred while processing {video_path}: {e}")
        return None



def sort_videos_by_date(video_files):
    video_files_with_dates = [(f, get_video_creation_date(f)) for f in video_files]
    video_files_with_dates = [(f, dt) for f, dt in video_files_with_dates if dt is not None]
    result = sorted(video_files_with_dates, key=lambda x: x[1])
    video_files = [f for f, dt in result]
    print(f"sort_videos_by_date function returning {video_files} to sort video files by date.")
    return video_files


def copy_videos_sorted(video_files):
    print(f"Entering copy_videos_sorted function to copy video files to videos_sorted directory.")
    sorted_directory = "videos_sorted"
    if not os.path.exists(sorted_directory):
        os.makedirs(sorted_directory)
    else:
        shutil.rmtree(sorted_directory)
        os.makedirs(sorted_directory)

    for video_path in video_files:
        creation_date = get_video_creation_date(video_path)
        if creation_date is None:
            print(f"Skipping {video_path} due to missing creation date.")
            continue

        file_name = os.path.splitext(os.path.basename(video_path))[0]
        ext = os.path.splitext(video_path)[1]
        new_file_name = creation_date.strftime("%Y-%m-%dT%H%M%S") + "_" + file_name + ext

        new_video_path = os.path.join(sorted_directory, new_file_name)
        shutil.copy2(video_path, new_video_path)
    return sorted_directory


def extract_random_clips():
    clips_directory = "video_clips"
    sorted_directory = "videos_sorted"

    if not os.path.exists(clips_directory):
        os.makedirs(clips_directory)
    else:
        shutil.rmtree(clips_directory)
        os.makedirs(clips_directory)

    sorted_video_files = [os.path.join(sorted_directory, f) for f in os.listdir(sorted_directory) if is_video(f)]

    for sorted_video_path in sorted_video_files:
        video = VideoFileClip(sorted_video_path)
        video_duration = video.duration
        random_start = random.uniform(0, max(0, video_duration - 2))  # Ensure random_start stays within the video's duration
        clip = video.subclip(random_start, min(video_duration, random_start + 2))  # Ensure the end time doesn't exceed the video's duration

        file_name, ext = os.path.splitext(os.path.basename(sorted_video_path))
        new_file_name = f"{file_name}_clip{ext}"
        new_clip_path = os.path.join(clips_directory, new_file_name)
        clip.write_videofile(new_clip_path, codec='libx264', audio_codec='aac')



def main():
    parser = argparse.ArgumentParser(description='Recursively find all video files in a directory, sort them by creation date, and copy them to a new directory with a new naming convention.')
    parser.add_argument('directory', type=str, help='the directory to search for video files')
    args = parser.parse_args()


    video_directory = args.directory
    video_files = find_videos(video_directory)
    sort_videos_by_date(video_files)
    copy_videos_sorted(video_files)
    extract_random_clips()

if __name__ == '__main__':
    main()





