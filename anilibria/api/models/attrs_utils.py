__all__ = ["convert", "convert_list", "convert_playlist"]


def convert(obj):
    def wrapper(kwargs):
        if kwargs is None:
            return None
        return obj(**kwargs)

    return wrapper


def convert_list(obj):
    def wrapper(list):
        if list is None:
            return []
        return [obj(**_) for _ in list]

    return wrapper


def convert_playlist(obj):
    def wrapper(playlist: dict):
        return [obj(**_) for _ in playlist.values()]

    return wrapper
