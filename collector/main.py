"""
Collector Service — Layer 1
Probes API endpoints and pushes results to the queue.
"""
import asyncio
import time
from datetime import datetime, timezone

import httpx


async def probe(client: httpx.AsyncClient, url: str) -> dict:
    """
    Probe a single URL using a shared HTTP client.
    """
    start = time.perf_counter()
    try:
        response = await client.get(url)
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "url": url,
            "status_code": response.status_code,
            "latency_ms": round(latency_ms, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": None,
        }
    except httpx.TimeoutException:
        return {
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": "timeout",
        }
    except httpx.ConnectError:
        return {
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": "connection_error",
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "latency_ms": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
        }


async def main():
    urls = [
        "https://api.github.com",
        "https://httpbin.org/get",
        "https://this-does-not-exist-xyz123.com",
    ]

    async with httpx.AsyncClient(timeout=10.0) as client:
        start = time.perf_counter()
        results = await asyncio.gather(*[probe(client, url) for url in urls])
        total = (time.perf_counter() - start) * 1000

    for r in results:
        print(r)
    print(f"\nTotal time for {len(urls)} URLs: {total:.2f}ms")


if __name__ == "__main__":
    asyncio.run(main())