from typing import List


class Config:
    def __init__(self, dev_key: str, engine_key: str, precision: float, query: List[str]):
        self.dev_key = dev_key
        self.engine_key = engine_key
        self.precision = precision
        self.query = query
