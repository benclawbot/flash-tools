#!/usr/bin/env python3
"""
Open Brain client for Flash - stores and retrieves memories.
"""
import os
import requests
from typing import List, Dict, Optional

OPENBRAIN_URL = os.environ.get("OPENBRAIN_URL", "http://localhost:8000")

def store_memory(content: str, source: str = "flash", tags: List[str] = None, importance: float = 0.7) -> Dict:
    """Store a memory in Open Brain."""
    resp = requests.post(
        f"{OPENBRAIN_URL}/memories",
        json={
            "content": content,
            "source": source,
            "tags": tags or [],
            "importance": importance
        }
    )
    resp.raise_for_status()
    return resp.json()

def search_memories(query: str, limit: int = 5) -> List[Dict]:
    """Search memories in Open Brain."""
    resp = requests.post(
        f"{OPENBRAIN_URL}/memories/search",
        json={"query": query, "limit": limit}
    )
    resp.raise_for_status()
    return resp.json()

def get_stats() -> Dict:
    """Get Open Brain stats."""
    resp = requests.get(f"{OPENBRAIN_URL}/stats")
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    # Test
    print("Testing Open Brain connection...")
    stats = get_stats()
    print(f"Stats: {stats['total']} memories")
    
    # Store test
    result = store_memory("Flash connected to Open Brain!", source="flash", tags=["test", "connection"])
    print(f"Stored: {result['id']}")
    
    # Search
    results = search_memories("Flash")
    print(f"Found: {len(results)} memories")
