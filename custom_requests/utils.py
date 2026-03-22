import urllib.parse


def str2wb_quote(src: str) -> str:
    """Make quote string as in WB"""
    return "+".join([urllib.parse.quote(s) for s in src.split(" ")])
