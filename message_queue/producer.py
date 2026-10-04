"""
Redis producer — result ko Redis Stream mein daalta hai.
"""
import redis


# Module-level variable. Pehli baar None, baad mein Redis client.
_redis_client = None


def get_redis():
    """
    Redis connection return karta hai.
    Pehli baar naya banata hai, baad mein wahi reuse karta hai.
    """
    global _redis_client
    
    if _redis_client is None:
        # Pehli baar — naya client banao
        _redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
    
    return _redis_client


def push_probe_result(result: dict) -> str:
    """
    Result dict ko Redis Stream 'probes' mein daalta hai.
    Entry ID return karta hai.
    """
    r = get_redis()
    
    # Redis sirf string values leta hai.
    # Isliye har value ko string mein convert karo.
    string_data = {k: str(v) for k, v in result.items()}
    
    # XADD — Stream mein entry add karo
    # 'probes' = stream ka naam
    # '*' = auto-generate ID (timestamp based)
    entry_id = r.xadd("probes", string_data)
    
    return entry_id