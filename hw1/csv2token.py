# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
脚本功能：
转换 ebook.csv --> tokens.csv

遗留问题:
 对于body的解析，目前的做法是一次性加载body所有字符串，
当body过大时，可能是有问题的
"""
import sys
import csv


def parse_words(body):
    words = []
    offset = 0
    length = len(body)

    # Init offset to the first position that body[offset] is a alphabet chacater
    while offset < length and not body[offset].isalpha():
        offset += 1
    if offset == length:
        return []

    while offset < length:
        start = offset
        end = start
        while end < length and body[end].isalpha():
            end += 1
        words.append(body[start:end])
        # init to next word
        offset = end
        while offset < length and not body[offset].isalpha():
            offset += 1
    return words


if __name__ == '__main__':
    file_name = 'ebook.csv'
    rd = open(file_name, 'r', encoding='ISO-8859-1')
    wd = open('tokens.csv', 'w', newline='', encoding='ISO-8859-1')
    csv.field_size_limit(sys.maxsize)
    csv_header = ['title', 'author', 'release_date', 'ebook_id', 'language', 'body']
    csv_reader = csv.DictReader(rd, csv_header)
    token_header = ['ebook_id', 'token']
    csv_writer = csv.DictWriter(wd, token_header)
    csv_writer.writeheader()

    # convert csv to tokens.csv
    for idx, row in enumerate(csv_reader):
        if idx == 0:
            continue
        body = row['body']
        words = parse_words(body)
        id = row['ebook_id']
        for word in words:
            csv_writer.writerow({'ebook_id': id, 'token': str(word).lower()})

    rd.close()
    wd.close()
