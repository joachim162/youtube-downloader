import ffmpeg


def concat(video_path: list, audio_path: list, video_title: str, target_dir: str) -> None:
    """
    Merge video and audio to one file

    :param video_path: path to video file
    :param audio_path: path to audio file
    :param video_title: name of video
    :param target_dir: target directory
    :return: None
    """
    # TODO: Re-implement method
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    # variables {v} and {a} are parameters for a number of streams
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{target_dir}/CONVERTED{video_title}').run()
