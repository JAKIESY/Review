#! /usr/local/bin/python3
# coding:utf-8
import random
from conf import *
from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, client):
        self.client = client
        self.collection = None

    def create_collection(self, db_name, collection):
        db = self.client.get_database(db_name)
        return db.create_collection(collection)

    def insert_data(self, db_name, collection, data):
        self.client.get_database(db_name)[collection].insert_one(data)

    def show_data(self, db_name, collection):
        for result in self.client.get_database(db_name)[collection].find():
            print(result)

    def save_data(self):
        pass

    def drop_collection(self):
        pass

    def drop_db(self):
        pass


class Review(object):
    def __init__(self, client):
        self.client = client

    def cnt_dbs(self):
        learning_db = list(set(self.client.list_database_names()) - set(NOT_NEED_DBS))
        return learning_db, len(learning_db)

    def cnt_table(self, db):
        collection_list = self.client.get_database(db).list_collection_names()
        return collection_list, len(collection_list)


class ReviewStrategy(Review):
    # todo: 最新的记录应该优先复习，所以最新的数据概率要大些
    # todo: 数据库内容与本地Excel文档同步，进行数据备份
    def __init__(self, client, db, num_table, num_doc):
        Review.__init__(self, client)
        self.db = db
        self.num_table = num_table
        self.num_doc = num_doc

    def random_select_table(self):
        if self.num_table > self.cnt_table(self.db)[1]:
            raise ParamException("the number of db should no more than {}".format(self.cnt_table(self.db)[1]))
        return random.sample(self.cnt_table(self.db)[0], k=self.num_table)

    def random_select_doc(self):
        for single_table in self.random_select_table():
            print('{}:'.format(single_table))
            # use $project to avoid outputting _id
            for i in self.client[self.db][single_table].aggregate(
                    [{'$sample': {'size': self.num_doc}}, {"$project": {'_id': 0}}]):
                print(i)
            print('\n')


class ParamException(Exception):
    pass


db_client = MongoClient(host='localhost', port=27017)
print("all the databases are: {}\n".format(db_client.list_database_names()))
print(ReviewStrategy(db_client, 'python', 3, 3).random_select_doc())
