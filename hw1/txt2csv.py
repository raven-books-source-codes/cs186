# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import csv

"""
脚本功能：
转换ebooks_xxx.txt --> ebooks.csv
"""


def get_one_entry(rd):
    """
    从rd中，生成一个csv row

    Returns: entry
            如果 entry = empty, 说明rd代表的文件无法生成一个有效entry
    """
    # Read txt file
    one_entry = {}
    while True:
        one_line = rd.readline()

        if one_line == '':  # 读取循环退出
            break

        if one_line.startswith('Title:'):
            if len(one_entry) != 0:
                break
            else:
                one_entry = {
                    'title': 'null',
                    'author': 'null',
                    'release_date': 'null',
                    'ebook_id': 'null',
                    'language': 'null',
                    'body': 'null'
                }

            tmp = one_line[len('Title:'):]
            one_entry['title'] = tmp.strip()

        elif one_line.startswith('Author:'):
            tmp = one_line[len('Author:'):]
            one_entry['author'] = tmp.strip()

        elif one_line.startswith('Release Date:'):
            tmp = one_line[len('Release Date:'):]
            tmp = tmp.strip()
            # tmp contains release data and ebook id
            idx = tmp.find('[')
            assert (idx != -1)
            release_data = tmp[:idx - 1]

            idx = tmp.rfind('#')
            assert (idx != -1)
            ebook_id = tmp[idx + 1:-1]

            one_entry['release_date'] = release_data.strip()
            one_entry['ebook_id'] = ebook_id.strip()

        elif one_line.startswith('Language:'):
            tmp = one_line[len('Language:'):]
            one_entry['language'] = tmp.strip()
        elif one_line.startswith('*** START OF THE PROJECT GUTENBERG'):
            buffer = []
            while True:
                tmp_line = rd.readline()
                if tmp_line == '':
                    break
                if tmp_line.startswith('*** END OF THE PROJECT GUTENBERG'):
                    break
                buffer.append(tmp_line)
            one_entry['body'] = "\r\n".join(buffer)
            break

    return one_entry


if __name__ == '__main__':
    assert(len(sys.argv) == 2)
    file_name = sys.argv[1]
    rd = open(file_name, 'r', encoding='ISO-8859-1')
    wd = open('ebook.csv', 'w', newline='', encoding='ISO-8859-1')
    header = ['title', 'author', 'release_date', 'ebook_id', 'language', 'body']
    csv_writer = csv.DictWriter(wd, header)
    csv_writer.writeheader()

    cnt = 0
    while True:
        one_entry = get_one_entry(rd)
        if len(one_entry) == 0:
            break
        cnt = cnt + 1
        # one_entry['body'] = 'null'
        csv_writer.writerow(one_entry)
    print(cnt)

    wd.close()
    rd.close()
