from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.core.constants import ERROR_INVALID_DATE_FORMAT
from src.repositories.benchmark_repository import BenchmarkRepository
from src.services.benchmark import BenchmarkService

router = APIRouter()

repository = BenchmarkRepository()
service = BenchmarkService(repository)


@router.get("/results/average")
def get_average_results():
    return service.calculate_average()


@router.get("/results/average/{start_time}/{end_time}")
def get_average_results_within_window(start_time: str, end_time: str):
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError:
        raise HTTPException(status_code=400, detail=ERROR_INVALID_DATE_FORMAT)
    return service.calculate_average(start_dt, end_dt)
