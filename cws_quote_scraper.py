#!usr/bin/python

# import re

from db_ops import update_database
from utils import get_page_contents


def get_quotes():
    url = "http://advaitaashrama.org"
    contents = get_page_contents(url)
    blockquote_end_index = contents.find("</blockquote>")
    contents = contents[blockquote_end_index:]
    paragraph_start_index = contents.find("<p>")
    paragraph_end_index = contents.find("</p>")
    quote = contents[paragraph_start_index + 3:paragraph_end_index].strip()
    print quote
    update_database(quote)


def regex_attempt():
    url = "http://advaitaashrama.org"
    contents = get_page_contents(url)
    print contents


if __name__ == '__main__':
    get_quotes()
    # regex_attempt()
