# SuperBenchmark

SuperBenchmark is a FastAPI application designed to manage and query benchmarking results for a Large Language Model (LLM). The application provides an API for retrieving performance statistics.

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Get Average Results](#1-get-average-results)
  - [Get Average Results within a Time Window](#2-get-average-results-within-a-time-window)
- [Testing](#testing)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/elsbrd/superbenchmark.git
   cd src
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or for Windows:
   venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file inside the `src` folder with the following content:
   ```env
   SUPERBENCHMARK_DEBUG=True
   ```

---

## Configuration

The application supports a debug mode, controlled via the `SUPERBENCHMARK_DEBUG` environment variable:

- `SUPERBENCHMARK_DEBUG=True`: Uses the `test_database.json` file as the data source.
- `SUPERBENCHMARK_DEBUG=False`: Raises a `NotImplementedError`, as production mode is not yet implemented.

---

## Running the Application

To run the application in debug mode:

```bash
uvicorn src.main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

---

## Project Structure

- `src/` - Main application code.
- `core/` - Application settings and constants.
- `repositories/` - Data handling functions.
- `schemas/` - Data validation and serialization.
- `routes/` - API endpoints.
- `services/` - Business logic.

---

## API Endpoints

### 1. Get Average Results

**GET /results/average**

Returns the average performance statistics across all benchmarking results.

Example request using `curl`:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/results/average' \
  -H 'accept: application/json'
```

Example response:

```json
{
  "average_token_count": 10.2,
  "average_time_to_first_token": 210.0,
  "average_time_per_token": 27.6,
  "average_total_generation_time": 485.2
}
```

---

### 2. Get Average Results within a Time Window

**GET /results/average/{start_time}/{end_time}**

Returns the average performance statistics for results recorded within a specified time window.

Example request using `curl`:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/results/average/2024-06-01T00:00:00/2024-06-02T00:00:00' \
  -H 'accept: application/json'
```

Example response:

```json
{
  "average_token_count": 8.4,
  "average_time_to_first_token": 190.0,
  "average_time_per_token": 25.8,
  "average_total_generation_time": 460.4
}
```

#### Possible Errors:
- **400 Bad Request**: Invalid date format.
- **404 Not Found**: No results found in the given time window.

---

## Testing

To run tests with `pytest`:

```bash
pytest
```

---