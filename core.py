import concurrent.futures
import uvicorn
import os
import subprocess

from api import app


# Function to run the FastAPI server
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Worker function
def run_worker():
    worker_path = os.path.join("worker", "main.py")
    subprocess.run(["python", worker_path])


# Run both FastAPI and the worker concurrently
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(run_fastapi)
        executor.submit(run_worker)
