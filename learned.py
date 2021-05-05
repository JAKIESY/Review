#! /usr/local/bin/python3
# coding:utf-8

import argparse
from pymongo import MongoClient
from python_review import MongoDB

# 创建解析器
# todo: 修改数据库信息
parser = argparse.ArgumentParser()
parser.add_argument('-a', nargs=3, help='python3 learned.py -a <db> <collection> dict')
args = parser.parse_args()

key = args.a[-1][1:-1].split(':')[0]
val = args.a[-1][1:-1].split(':')[1]

data = dict()
data[key] = val
MongoDB(MongoClient(host='localhost', port=27017)).insert_data(args.a[0], args.a[1], data)





