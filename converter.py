import os.path

import ffmpeg


# TODO: Fix concat method
# ffmpeg probably wants absolute path only
def concat(video_path: str, audio_path: str, video_title: str, target_dir: str):
    print(f'Video abs path: {video_path}\n audio path: {audio_path}')
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    # variables v and a are parameters for a number of streams
    print(f'{target_dir}/CONVERTED{video_title}')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{target_dir}/CONVERTED{video_title}').run()
