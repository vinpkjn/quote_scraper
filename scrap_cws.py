#!usr/bin/python

import re
import requests
# import json
from BeautifulSoup import BeautifulSoup

from utils import find_index


url = r"http://advaitaashrama.org/cw/content.php"
baseURL = r"http://advaitaashrama.org/cw/"

table_of_contents = {}
volume = None
chap = None
sub_chap = None
PRE_MNU_POS = 1
is_fix_mnu_pos = False
FLAG = False
count = 0


def main():
    menu_list = get_table_of_contents()
    make_table_of_contents(menu_list)
    return table_of_contents
    # beautyfulrasam()


def beautyfulrasam():
    html_content = requests.get(url)
    print html_content
    soup = BeautifulSoup(html_content.text)
    print "vinod"
    # rytvidu = soup
    script = soup.findall('script').string
    print script


def get_table_of_contents():
    html_content = requests.get(url)
    regex_pattern = re.compile('menu\.entry\([^;]*')
    menu_list = re.findall(regex_pattern, html_content.content)
    return menu_list


def make_table_of_contents(menu_list):
    global count
    global FLAG
    tree_pos = None
    head = None
    head_desc = None
    topic_url = None
    menu_itm_txt = None

    if menu_list:
        for menu_item in menu_list:
            # TODO convert string parsing to regex
            # find menu position(tree_pos)
            index_pos = find_index(menu_item, '(') + 1
            tree_pos = menu_item[index_pos:index_pos + 1]

            # find the head, head desc
            menu_itm_txt = menu_item[index_pos:]
            index_pos = find_index(menu_itm_txt, '"') + 1
            end_pos = find_index(menu_itm_txt, '"', index_pos)
            head_desc = menu_itm_txt[index_pos: end_pos]
            head = head_desc.translate(None, ":,'")
            head = head.replace(" ", "_")

            # find topic_url
            index_pos = find_index(menu_itm_txt, '"', end_pos + 1)
            end_pos = find_index(menu_itm_txt, '"', end_pos + 1 + 1)
            menu_itm_txt = menu_itm_txt[index_pos:]
            index_pos = find_index(menu_itm_txt, '"')

            if index_pos > -1:
                end_pos = find_index(menu_itm_txt, '"', index_pos + 1)
                topic_url = menu_itm_txt[index_pos + 1:end_pos]
            else:
                menu_itm_txt = None
                topic_url = None

            count += 1

            # if head == "Volume_2":
            #     FLAG = True
            # elif head == "Volume_3":
            #     FLAG = False

            # if FLAG:
            build_dictionary(tree_pos, head, head_desc, topic_url)
            # print tree_pos, 3*'=', head, 3*'=', head_desc, 3*'=', topic_url
            # if count > 56 and count < 65:
            # print tree_pos, 3*'=', head, 3*'=', head_desc, 3*'=', topic_url
            # print json.dumps(table_of_contents)


def build_dictionary(mnu_pos, head, head_desc, topic_url):
    global PRE_MNU_POS
    mnu_pos = int(mnu_pos)

    try:
        if head[:7] == "Volume_":
            global volume
            global chap
            global sub_chap

            volume = head
            chap = None
            sub_chap = None

            table_of_contents[head] = [head_desc, topic_url, {}]
        else:
            mnu_pos = fix_menu_level(mnu_pos)
            add_chapters(mnu_pos, head, head_desc, topic_url)

        # print table_of_contents
        # print mnu_pos, 3*'=', PRE_MNU_POS, 3*'=', head, 3*'='
        # , head_desc, 3*'=', topic_url
        # print mnu_pos, 3*'=', head, 3*'=', head_desc, 3*'=', topic_url
    except Exception as ex:
        raise ex


def fix_menu_level(mnu_pos):
    global PRE_MNU_POS

    if mnu_pos == PRE_MNU_POS:
        PRE_MNU_POS = mnu_pos
    elif mnu_pos > PRE_MNU_POS:
        if mnu_pos - 1 != PRE_MNU_POS:
            mnu_pos = PRE_MNU_POS + 1
        else:
            PRE_MNU_POS = mnu_pos
    elif mnu_pos < PRE_MNU_POS:
        PRE_MNU_POS = mnu_pos

    return mnu_pos


def add_chapters(mnu_pos, head, head_desc, topic_url):
    # global PRE_MNU_POS
    arr = [head_desc, topic_url, {}]

    try:
        if volume:
            mnu_pos = int(mnu_pos)
            if mnu_pos == 2:
                global chap
                chap = head
                # PRE_MNU_POS = mnu_pos
                table_of_contents[volume][2][head] = arr
            elif mnu_pos == 3:
                global sub_chap
                sub_chap = head
                # PRE_MNU_POS = mnu_pos
                table_of_contents[volume][2][chap][2][head] = arr
            elif mnu_pos == 4:
                # PRE_MNU_POS = mnu_pos
                table_of_contents[volume][2][chap][2][sub_chap][2][head] = arr
    except Exception as ex:
        raise ex

def fix_num(PRE_MNU_POS, mnu_pos):
    '''
    little hack to workaround bogus menu sequencing in the source site
    '''

    global is_fix_mnu_pos

    if PRE_MNU_POS != mnu_pos and (PRE_MNU_POS + 1) != mnu_pos:
        is_fix_mnu_pos = True
        return PRE_MNU_POS + 1
    elif PRE_MNU_POS != mnu_pos and (PRE_MNU_POS - 1) >= mnu_pos:
        is_fix_mnu_pos = False
        return mnu_pos
    elif PRE_MNU_POS == mnu_pos:
        return mnu_pos - 1

    if is_fix_mnu_pos:
        return PRE_MNU_POS


if __name__ == '__main__':
    main()
