import os
import librosa
import json

def generate_beats(configs):
    os.makedirs(configs['temp_audio_configs'], exist_ok=True)

    audio_files = [f for f in os.listdir(configs["audio_files"]) if f.endswith(".wav") or f.endswith(".mp3")]

    for file_name in audio_files:
        audio_path = os.path.join(configs['audio_files'], file_name)
        y, sr = librosa.load(audio_path)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        json_data = []
        sequence_number = 1

        for i in range(1, len(beat_frames)):
            duration_from_last = librosa.frames_to_time(beat_frames[i] - beat_frames[i - 1], sr=sr)
            json_data.append({
                "sequence_number": sequence_number,
                "duration_from_last": duration_from_last
            })
            sequence_number += 1

        json_path = os.path.join(configs['temp_audio_configs'], f'{file_name.split(".")[0]}-beats.json')

        with open(json_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Generated JSON file: {json_path}")
