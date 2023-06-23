import os
import read_configs
import get_beats
import match_source_video

configs = read_configs.read_environment()
print(f"Read configs: {configs}")

get_beats.generate_beats(configs)
match_source_video.generate_video_cuts(configs)