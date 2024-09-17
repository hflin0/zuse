from pathlib import Path

def get_snippet_dir():
    return Path.absolute(Path(__file__).parent)