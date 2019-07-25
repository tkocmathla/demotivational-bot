from difflib import SequenceMatcher


# https://stackoverflow.com/a/17388505
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
