#!/usr/bin/env python3
# test_clustering.py
# Quick script to test clustering locally

import sys
sys.path.insert(0, '.')

from analysis import perform_clustering

print("Testing clustering...")
result = perform_clustering()

if result:
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        print(f"Data points: {len(result.get('data', []))}")
        print(f"Summary: {result.get('summary')}")
    else:
        print(f"Message: {result.get('message')}")
else:
    print("Result is None")