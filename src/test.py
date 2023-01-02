def is_resolution(resolution: str):
    """
    Check if resolution from argument is a valid YT resolution
    :param resolution:
    :type resolution:
    :return:
    :rtype:
    """
    # TODO: Test the functionality
    # TODO: Change the list of resolutions to str, pytube accepts resolution in "1080p" format
    # TODO: Implement a check that resolution is in valid format before searching it in list
    value = resolution
    if value[-1] == 'p':
        return True
    return False


print(is_resolution("1080p"))
