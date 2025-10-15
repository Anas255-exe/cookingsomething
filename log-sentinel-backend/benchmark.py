"""Quick benchmark tool for Log Sentinel endpoints."""

import argparse
import asyncio
import statistics
import time
from typing import Iterable

import httpx

DEFAULT_URL = "http://127.0.0.1:8000"
DEFAULT_ENDPOINTS = ["/status", "/logs", "/alerts", "/report/csv"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark Log Sentinel API")
    parser.add_argument("--base-url", default=DEFAULT_URL, help="Server base URL")
    parser.add_argument("--runs", type=int, default=20, help="Total requests per endpoint")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrent request limit")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds")
    parser.add_argument(
        "--endpoints",
        nargs="*",
        help="Space separated list of endpoints; defaults to builtin set",
    )
    return parser.parse_args()


async def exercise_endpoint(
    client: httpx.AsyncClient, url: str, runs: int, concurrency: int
) -> tuple[list[float], float]:
    timings: list[float] = []
    semaphore = asyncio.Semaphore(max(1, concurrency))

    async def single_call() -> None:
        async with semaphore:
            start = time.perf_counter()
            response = await client.get(url)
            response.raise_for_status()
            timings.append(time.perf_counter() - start)

    start_batch = time.perf_counter()
    await asyncio.gather(*(single_call() for _ in range(runs)))
    elapsed = time.perf_counter() - start_batch
    return timings, elapsed


def compute_p95(samples: Iterable[float]) -> float:
    data = list(samples)
    if not data:
        return 0.0
    if len(data) == 1:
        return data[0]
    return statistics.quantiles(data, n=100, method="inclusive")[94]


async def run_benchmark(
    base_url: str,
    runs: int,
    concurrency: int,
    timeout: float,
    endpoints: list[str],
) -> None:
    async with httpx.AsyncClient(timeout=timeout) as client:
        for endpoint in endpoints:
            url = f"{base_url.rstrip('/')}{endpoint}"
            timings, elapsed = await exercise_endpoint(client, url, runs, concurrency)
            mean = statistics.mean(timings) if timings else 0.0
            p95 = compute_p95(timings)
            rps = runs / elapsed if elapsed else float("inf")
            print(
                f"{endpoint:12s} count={runs:3d} conc={concurrency:2d} "
                f"latency_mean={mean*1000:.2f}ms latency_p95={p95*1000:.2f}ms "
                f"throughput={rps:.1f} req/s"
            )


def main() -> None:
    args = parse_args()
    endpoints = args.endpoints if args.endpoints else DEFAULT_ENDPOINTS
    asyncio.run(
        run_benchmark(
            base_url=args.base_url,
            runs=args.runs,
            concurrency=args.concurrency,
            timeout=args.timeout,
            endpoints=endpoints,
        )
    )


if __name__ == "__main__":
    main()
