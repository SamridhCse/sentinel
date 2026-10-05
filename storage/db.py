"""
TimescaleDB storage — probe results ko database mein daalta hai.
"""
import psycopg


# Module-level variable. Pehli baar None, baad mein connection.
_conn = None


def get_connection():
    """
    PostgreSQL connection return karta hai.
    Pehli baar naya banata hai, baad mein wahi reuse karta hai.
    """
    global _conn
    
    if _conn is None:
        # Pehli baar — naya connection banao
        _conn = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="sentinel",
            user="postgres",
            password="devpassword"
        )
    
    return _conn


def insert_probe(data: dict):
    """
    Ek probe result dict ko 'probes' table mein insert karta hai.
    
    Input example:
        {
            "timestamp": "2026-10-04T12:39:00+00:00",
            "url": "https://api.github.com",
            "status_code": "200",
            "latency_ms": "145.3",
            "error": "None"
        }
    
    Note: Redis se sab values string aate hain.
    Isliye status_code ko int, latency_ms ko float mein convert karna hai.
    """
    conn = get_connection()
    
    # String se actual value mein convert karo
    status_code = int(data["status_code"]) if data["status_code"] != "None" else None
    latency_ms = float(data["latency_ms"]) if data["latency_ms"] != "None" else None
    error = None if data["error"] == "None" else data["error"]
    
    # Cursor banao — SQL chalane ke liye
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO probes (time, url, status_code, latency_ms, error)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["timestamp"],
                data["url"],
                status_code,
                latency_ms,
                error,
            )
        )
    
    # Commit — warna data save nahi hoga
    conn.commit()