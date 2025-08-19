import subprocess
import os

def convert_video(source, resolution):
    file_dir = os.path.dirname(source)
    file_name, file_ext = os.path.splitext(os.path.basename(source))
    new_file_name = f"{file_name}_{resolution}.mp4"
    new_file_path = os.path.join(file_dir, new_file_name)

    cmd = f"ffmpeg -i '{source}' -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 '{new_file_path}'"
    run = subprocess.run(cmd, capture_output=True, shell=True)
    print(run.stdout)
    print(run.stderr)
