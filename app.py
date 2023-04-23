from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
video_clips_dir = 'static/video_clips'
video_files = sorted([os.path.join(video_clips_dir, f) for f in os.listdir(video_clips_dir) if os.path.isfile(os.path.join(video_clips_dir, f))])

# Global variables for the current index and total number of videos
current_index = 0
total_videos = len(video_files)

def get_previous_video():
    global current_index
    previous_index = (current_index - 1) % total_videos
    return video_files[previous_index]

def update_video_files():
    global video_files, total_videos
    video_files = sorted([os.path.join(video_clips_dir, f) for f in os.listdir(video_clips_dir) if os.path.isfile(os.path.join(video_clips_dir, f))])
    total_videos = len(video_files)

@app.route('/')
def index():
    global current_index

    if not video_files:
        all_videos = [os.path.join(video_clips_dir, f) for f in os.listdir(video_clips_dir) if os.path.isfile(os.path.join(video_clips_dir, f))]
        return render_template('play_all.html', video_files=all_videos)
    
    video_file = video_files[current_index]
    return render_template('index.html', video_file=video_file)

@app.route('/remove', methods=['POST'])
def remove_video():
    global current_index
    video_to_remove = request.form['video_to_remove']
    os.remove(video_to_remove)
    update_video_files()
    current_index = (current_index) % total_videos
    return redirect(url_for('index'))

@app.route('/previous', methods=['POST'])
def previous_video():
    global current_index
    current_index = (current_index - 1) % total_videos
    return redirect(url_for('index'))

@app.route('/keep', methods=['POST'])
def keep_video():
    global current_index
    current_index = (current_index + 1) % total_videos
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
