$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

.\.venv\Scripts\python.exe scripts\generate_data.py
.\.venv\Scripts\python.exe scripts\train.py
.\.venv\Scripts\python.exe scripts\benchmark_api.py
.\.venv\Scripts\python.exe -m pytest
