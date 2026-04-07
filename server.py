from fastmcp import FastMCP
from config import Config
from dbclient import DbClient

mcp = FastMCP("FinInsights", instructions="MongoDB connector for NOQ Orders")


@mcp.tool
def get_orders_by_order_num(orderNum: str):
    "Gets key present at order level schema with a value and finds a matching order"
    print(f'input params: {orderNum}')
    config = Config()
    client = DbClient(config)
    return client.get_order_by_filter("orderNum", orderNum)
