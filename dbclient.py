from pymongo import MongoClient
from config import Config
from orderSchema import Order
from pymongo.collection import Collection
from datetime import datetime, date, time


class DbClient():

    def __init__(self, config: Config):
        self.client = MongoClient(config.DB_URI)
        self.database = self.client['local']
        self.orders: Collection[Order] = self.database['orders']

    def get_order_by_key(self, key: str, value: str):
        return self.orders.find_one({
            key: value
        })

    def get_order_by_filter(self, date: date, filter_dict: dict, limit: int = 20):
        start_date = datetime.combine(date, time.min)
        end_date = datetime.combine(date, time.max)
        query = filter_dict
        query["created_at"] = {"$gte": start_date, "$lt": end_date}
        return self.orders.find(query).limit(limit)

    def run_aggregation(self, pipeline: list[dict]):
        return self.orders.aggregate(pipeline)
