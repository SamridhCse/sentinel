"""
Redis consumer — Stream se messages padhta hai aur TimescaleDB mein daalta hai.
"""
import redis

# DB insert function import karo
from storage.db import insert_probe


def start_consumer():
    """
    'probes' stream se messages padhta rehta hai.
    Har message DB mein insert karta hai.
    """
    # Redis se connect
    r = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    
    print("Listening on 'probes' stream... (Ctrl+C to stop)")
    
    # last_id = jahan tak padh chuke.
    # "0" matlab shuru se padho.
    last_id = "0"
    
    while True:
        # XREAD — stream se padho
        messages = r.xread(
            {"probes": last_id},
            block=2000,
            count=10
        )
        
        if messages:
            for stream_name, entries in messages:
                for entry_id, data in entries:
                    # Screen pe print karo
                    print(f"[{entry_id}] {data['url']}")
                    
                    # DB mein insert karo
                    try:
                        insert_probe(data)
                    except Exception as e:
                        print(f"  DB insert failed: {e}")
                    
                    # last_id update karo
                    last_id = entry_id


if __name__ == "__main__":
    start_consumer()