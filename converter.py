import ffmpeg


def concat(video_path: str, audio_path: str, target_dir: str):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    # variables v and a are parameters for a number of streams
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished.mp4').run()
