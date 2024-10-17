import json
from datetime import datetime
from typing import List, Optional

from src.core.constants import TEST_DATABASE_PATH
from src.schemas.benchmark import BenchmarkResultSchema


class BenchmarkRepository:
    def __init__(self, file_path: str = TEST_DATABASE_PATH):
        self.file_path = file_path

    def load_data(self) -> List[BenchmarkResultSchema]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return [
            BenchmarkResultSchema(**result)
            for result in data["benchmarking_results"]
        ]

    def list_results(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[BenchmarkResultSchema]:
        results = self.load_data()
        if start_time and end_time:
            return [
                result
                for result in results
                if start_time <= result.timestamp <= end_time
            ]
        return results
