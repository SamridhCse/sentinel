"""
Redis consumer — Stream se messages padhta hai.
"""
import redis


def start_consumer():
    """
    'probes' stream se messages padhta rehta hai.
    Naye messages ke liye wait karta hai.
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
        # "probes" = stream ka naam
        # last_id = is ID ke BAAD se padho
        # block=2000 = 2 second wait karo agar naya message na ho
        # count=10 = ek baar mein max 10 messages
        messages = r.xread(
            {"probes": last_id},
            block=2000,
            count=10
        )
        
        if messages:
            # messages ka structure: [(stream_name, [(id, data), ...])]
            for stream_name, entries in messages:
                for entry_id, data in entries:
                    print(f"[{entry_id}] {data}")
                    
                    # last_id update karo — taaki next read pe duplicate na aaye
                    last_id = entry_id


# Sirf tab chalao jab direct is file ko run karo
if __name__ == "__main__":
    start_consumer()