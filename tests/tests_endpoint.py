from fastapi.testclient import TestClient

from src.main import app
from src.schemas.benchmark import BenchmarkResultSchema

client = TestClient(app)

test_data = {
    "benchmarking_results": [
        {
            "request_id": "1",
            "prompt_text": "Translate the following English text to French: 'Hello, how are you?'",
            "generated_text": "Bonjour, comment ça va?",
            "token_count": 5,
            "time_to_first_token": 150,
            "time_per_output_token": 30,
            "total_generation_time": 300,
            "timestamp": "2024-06-01T12:00:00",
        },
        {
            "request_id": "2",
            "prompt_text": "Summarize the following article: 'Artificial intelligence is transforming the world.'",
            "generated_text": "AI is changing the world.",
            "token_count": 6,
            "time_to_first_token": 200,
            "time_per_output_token": 25,
            "total_generation_time": 350,
            "timestamp": "2024-06-01T13:00:00",
        },
    ]
}


def mock_load_data(self):
    return [
        BenchmarkResultSchema(**result)
        for result in test_data["benchmarking_results"]
    ]


def test_get_average_results(monkeypatch):
    monkeypatch.setattr(
        "src.repositories.benchmark_repository.BenchmarkRepository.load_data",
        mock_load_data,
    )

    response = client.get("/results/average")
    assert response.status_code == 200
    data = response.json()

    assert data["average_token_count"] == 5.5
    assert data["average_time_to_first_token"] == 175
    assert data["average_time_per_token"] == 27.5
    assert data["average_total_generation_time"] == 325


def test_get_average_results_with_invalid_date_format():
    start_time = "invalid-date"
    end_time = "2024-06-01T23:59:59"

    response = client.get(f"/results/average/{start_time}/{end_time}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format"


def test_get_average_results_with_no_results(monkeypatch):
    monkeypatch.setattr(
        "src.repositories.benchmark_repository.BenchmarkRepository.load_data",
        mock_load_data,
    )

    start_time = "2023-01-01T00:00:00"
    end_time = "2023-01-01T23:59:59"

    response = client.get(f"/results/average/{start_time}/{end_time}")
    assert response.status_code == 404
    assert response.json()["detail"] == "No results found in this time window"


def test_get_average_results_varied_data(monkeypatch):
    varied_test_data = {
        "benchmarking_results": [
            {
                "request_id": "1",
                "prompt_text": "Translate the following English text to French: 'Hello, how are you?'",
                "generated_text": "Bonjour, comment ça va?",
                "token_count": 10,
                "time_to_first_token": 300,
                "time_per_output_token": 40,
                "total_generation_time": 400,
                "timestamp": "2024-06-01T12:00:00",
            },
            {
                "request_id": "2",
                "prompt_text": "Summarize the following article: 'Artificial intelligence is transforming the world.'",
                "generated_text": "AI is changing the world.",
                "token_count": 5,
                "time_to_first_token": 150,
                "time_per_output_token": 20,
                "total_generation_time": 250,
                "timestamp": "2024-06-01T13:00:00",
            },
        ]
    }

    def mock_varied_load_data(self):
        return [
            BenchmarkResultSchema(**result)
            for result in varied_test_data["benchmarking_results"]
        ]

    monkeypatch.setattr(
        "src.repositories.benchmark_repository.BenchmarkRepository.load_data",
        mock_varied_load_data,
    )

    response = client.get("/results/average")
    assert response.status_code == 200
    data = response.json()

    assert data["average_token_count"] == 7.5
    assert data["average_time_to_first_token"] == 225
    assert data["average_time_per_token"] == 30
    assert data["average_total_generation_time"] == 325


def test_get_results_within_valid_time_window(monkeypatch):
    monkeypatch.setattr(
        "src.repositories.benchmark_repository.BenchmarkRepository.load_data",
        mock_load_data,
    )

    start_time = "2024-06-01T00:00:00"
    end_time = "2024-06-01T13:30:00"

    response = client.get(f"/results/average/{start_time}/{end_time}")
    assert response.status_code == 200
    data = response.json()

    assert data["average_token_count"] == 5.5
    assert data["average_time_to_first_token"] == 175
    assert data["average_time_per_token"] == 27.5
    assert data["average_total_generation_time"] == 325


def test_no_results_within_time_window(monkeypatch):
    monkeypatch.setattr(
        "src.repositories.benchmark_repository.BenchmarkRepository.load_data",
        mock_load_data,
    )

    start_time = "2025-01-01T00:00:00"
    end_time = "2025-01-01T23:59:59"

    response = client.get(f"/results/average/{start_time}/{end_time}")
    assert response.status_code == 404
    assert response.json()["detail"] == "No results found in this time window"
