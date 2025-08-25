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

    hls_file_name = f"hls_{file_name}_{resolution}p.m3u8"
    hls_file_path = os.path.join(file_dir, hls_file_name)
    hls_file_cmd = f"ffmpeg -i '{new_file_path}' -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls '{hls_file_path}'"
    hls_run = subprocess.run(hls_file_cmd, capture_output=True, shell=True)
    print(hls_run.stdout)
    print(hls_run.stderr)
