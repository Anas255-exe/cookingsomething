"""
Demo script for Log Sentinel Backend

This script demonstrates how to interact with the Log Sentinel FastAPI backend
using HTTP requests. It assumes the FastAPI server is running locally on port 8000.

You can run this demo after starting the server with:
    uvicorn app.main:app --reload

Requirements:
    pip install requests
"""

import requests

BASE_URL = "http://localhost:8000"

def get_status():
    resp = requests.get(f"{BASE_URL}/status/")
    print("Service Status:", resp.json())

def get_logs():
    resp = requests.get(f"{BASE_URL}/logs/")
    print("Logs:", resp.json())

def get_alerts():
    resp = requests.get(f"{BASE_URL}/alerts/")
    print("Alerts:", resp.json())

def get_csv_report():
    resp = requests.get(f"{BASE_URL}/report/csv")
    print("CSV Report:")
    print(resp.text)

if __name__ == "__main__":
    print("=== Log Sentinel Backend Demo ===")
    get_status()
    get_logs()
    get_alerts()
    get_csv_report()
