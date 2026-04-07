import os
from dotenv import load_dotenv

load_dotenv()


class Config():

    def __init__(self) -> None:
        self.DB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
