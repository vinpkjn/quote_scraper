#!usr/bin/python
from urllib import urlopen


def get_page_contents(url):
    try:
        return urlopen(url).read()
    except:
        return None


def find_index(input, search_char, start_index=0):
    index = input.find(search_char, start_index)
    return index
