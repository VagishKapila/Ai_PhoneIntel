import random

def search_contractors(radius: int, trade: str):
    # Dummy placeholder list
    sample = [
        {"name": "Alpha Construction", "trade": trade, "distance": 3},
        {"name": "BuildMax Pro", "trade": trade, "distance": 7},
        {"name": "NextGen GC", "trade": trade, "distance": 11},
    ]

    return [c for c in sample if c["distance"] <= radius]