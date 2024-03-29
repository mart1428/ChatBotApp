import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime as dt 

class ChatHistoryDatabase():
    def __init__(self, host = 'localhost', port = 27017):
        self.client = MongoClient(host, port)

        self.db = self.client.chatbot
        self.collection = self.db.chat_history

    def retrieve_latest_document(self):
        if not self.is_empty():
            results = self.collection.find({}).sort('summary', pymongo.DESCENDING).limit(1)

            return results[0]
        
        else:
            return -1

    def show_recent_documents(self):
        for r in self.collection.find({}).limit(5):
            print(r)

    def is_empty(self):
        return self.collection.count_documents({}) == 0

    def insert_one_document(self, summary, prompt, history, mode):
        self.collection.insert_one({"summary" : summary, "timestamp" : dt.datetime.now(), "prompt" : prompt, "history" : history, 'mode' : mode})

    def update_chat_history(self, id, history):
        self.collection.update_one({"_id" : id }, {"$set" : {"history" : history, "timestamp" : dt.datetime.now()}})

    def delete_chat(self,id):
        self.collection.delete_one({'_id' : id})
        

if __name__ == "__main__":
    database = ChatHistoryDatabase()
    database.insert_one_document(summary = 'dummy', prompt = 'dummy', history = [''], mode = 0 )
    # print(database.update_chat_history(ObjectId('65c947553781b930be32bbae'), [[1]]))
    database.retrieve_latest_document()
