from datetime import datetime
from typing import List

from pydantic import BaseModel


class BenchmarkResultSchema(BaseModel):
    request_id: str
    prompt_text: str
    generated_text: str
    token_count: int
    time_to_first_token: int
    time_per_output_token: int
    total_generation_time: int
    timestamp: datetime


class BenchmarkingResultsSchema(BaseModel):
    benchmarking_results: List[BenchmarkResultSchema]
