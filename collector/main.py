"""
Collector Service — Layer 1
Probes API endpoints and pushes results to the queue.
"""
import asyncio
import httpx
from datetime import datetime, timezone
import time

async def probe(url: str) -> dict:
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
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
        return {"url": url, "status_code": None, "latency_ms": None,
                "timestamp": datetime.now(timezone.utc).isoformat(), "error": "timeout"}
    except httpx.ConnectError:
        return {"url": url, "status_code": None, "latency_ms": None,
                "timestamp": datetime.now(timezone.utc).isoformat(), "error": "connection_error"}
    except Exception as e:
        return {"url": url, "status_code": None, "latency_ms": None,
                "timestamp": datetime.now(timezone.utc).isoformat(), "error": str(e)}

# async def main():
#     result = await probe("https://api.github.com")
#     print(result)
# Test 1: Invalid URL (connection error)
# async def main():
#     result = await probe("https://this-does-not-exist-xyz123.com")
#     print(result)

# Test 2: Slow URL (timeout)
# async def main():
#     result = await probe("https://httpbin.org/delay/15")
#     print(result)


# Test 3: Parallel Probing (ye important hai)
async def main():
    urls = [
        "https://api.github.com",
        "https://httpbin.org/get",
        "https://this-does-not-exist-xyz123.com",
    ]
    
    start = time.perf_counter()
    results = await asyncio.gather(*[probe(url) for url in urls])
    total = (time.perf_counter() - start) * 1000
    
    for r in results:
        print(r)
    print(f"\nTotal time for 3 URLs: {total:.2f}ms")

if __name__ == "__main__":
    asyncio.run(main())