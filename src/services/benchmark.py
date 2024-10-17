from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from src.core.constants import ERROR_NO_RESULTS_FOUND
from src.repositories.benchmark_repository import BenchmarkRepository
from src.schemas.benchmark import BenchmarkResultSchema


class BenchmarkService:
    def __init__(self, repository: BenchmarkRepository):
        self.repository = repository

    def calculate_average(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> dict:
        results = self.repository.list_results(start_time, end_time)
        if not results:
            raise HTTPException(status_code=404, detail=ERROR_NO_RESULTS_FOUND)
        return self._calculate_average_from_results(results)

    def _calculate_average_from_results(
        self, results: List[BenchmarkResultSchema]
    ) -> dict:
        total_token_count = sum(r.token_count for r in results)
        total_time_to_first_token = sum(r.time_to_first_token for r in results)
        total_time_per_token = sum(r.time_per_output_token for r in results)
        total_gen_time = sum(r.total_generation_time for r in results)
        count = len(results)
        return {
            "average_token_count": total_token_count / count,
            "average_time_to_first_token": total_time_to_first_token / count,
            "average_time_per_token": total_time_per_token / count,
            "average_total_generation_time": total_gen_time / count,
        }
