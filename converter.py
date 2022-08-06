import os.path

import ffmpeg


# TODO: Fix concat method
# ffmpeg probably wants absolute path only
def concat(video_path: str, audio_path: str, target_dir: str = '.'):
    video_path = os.path.abspath(video_path)
    audio_path = os.path.abspath(audio_path)
    print(f'Video abs path: {video_path}\n audio path: {audio_path}')
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    # variables v and a are parameters for a number of streams
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished.mp4').run()


def format_path(self, paths: list) -> list:
    # TODO: Implement method that remove whitespaces from paths
    # TODO: Create solution that works on Linux and Windows
    paths[0] = paths[0].replace()
    return paths
