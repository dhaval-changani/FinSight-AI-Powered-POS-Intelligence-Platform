from pymongo import MongoClient
from config import Config


class DbClient():

    def __init__(self, config: Config):
        self.client = MongoClient(config.DB_URI)
        self.database = self.client['local']
        self.orders = self.database['orders']

    def get_order_by_filter(self, key: str, value: str):
        return self.orders.find_one({
            key: value
        })
