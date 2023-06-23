import os
import json
import glob

def generate_video_cuts(configs):
    print(f"generate_video_cuts()")
    print(f"Processing video files in directory: {configs['video_files']}")
    print(f"Processing audio meta files in directory: {configs['temp_audio_configs']}")

    # Create a list of sorted video files
    video_files = sorted(glob.glob(os.path.join(video_directory, '*')))
    print(f"Sorted video files: {video_files}")

    audio_meta_files = [f for f in os.listdir(audio_meta_directory) if f.endswith("-beats.json")]
    print(f"Audio meta files: {audio_meta_files}")

    total_duration = 0  # Initialize total duration counter

    for file_name in audio_meta_files:
        audio_meta_path = os.path.join(audio_meta_directory, file_name)

        with open(audio_meta_path, "r") as json_file:
            json_data = json.load(json_file)
            print(f"Loaded JSON data from: {audio_meta_path}")

            # Create a new list to hold the updated json data
            new_json_data = []

            # Assign video filename to each audio beat
            for i in range(min(len(json_data), len(video_files))):
                json_data[i]["source_video"] = video_files[i]
                total_duration += json_data[i]["duration_from_last"]
                print(f"Assigning source video {video_files[i]} to sequence number {json_data[i]['sequence_number']}")
                new_json_data.append(json_data[i])

            trailer_file_name = os.path.splitext(file_name)[0] + "-trailer.json"
            trailer_path = os.path.join(temp_configs_directory, trailer_file_name)

            os.makedirs(os.path.dirname(trailer_path), exist_ok=True)

            with open(trailer_path, "w") as trailer_file:
                trailer_meta = {
                    "trailer_duration": total_duration,
                    "clips": new_json_data
                }
                json.dump(trailer_meta, trailer_file, indent=4)
                print(f"Generated trailer JSON file: {trailer_path}")
