import json
from bson import ObjectId
from fastmcp import FastMCP
from config import Config
from dbclient import DbClient
from datetime import date

mcp = FastMCP("FinInsights", instructions="MongoDB connector for NOQ Orders")

config = Config()
client = DbClient(config)


def _serialize(doc) -> str:
    """Convert a MongoDB document (or None) to a JSON string."""
    if doc is None:
        return "null"
    return json.dumps(doc, default=lambda o: str(o) if isinstance(o, ObjectId) else repr(o))


@mcp.tool
def get_orders_by_order_num(orderNum: str) -> str:
    "Gets key present at order level schema with a value and finds a matching order"
    result = client.get_order_by_key("orderNum", orderNum)
    if result is None:
        return f"No order found with orderNum: {orderNum}"
    return _serialize(result)


@mcp.tool
def reconcile_order(orderNum: str, date: date) -> str:
    'Fetches one order using orderNum and check the data validation for that, returns errors if data is not correct, other wise returns order data in JSON format'
    cursor = client.get_order_by_filter(date, {"orderNum": orderNum}, 1)
    results = list(cursor)
    if not results:
        return f"No order found with orderNum: {orderNum} on {date}"
    return _serialize(results[0])
