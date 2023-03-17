#!/usr/bin/env python3
"""
Utility to reset a Redis cache
"""
import argparse
import cache

parser = argparse.ArgumentParser()
parser.add_argument(
    '--force',
    '--yes',
    '-f',
    '-y',
    action='store_true',
    help='skip confirmation prompt'
)
args = parser.parse_args()

if not args.force:
    confirmation = input("Are you sure you want to delete all data in the Redis cache? (Yes/No)")

if args.force or confirmation.lower() in ['yes', 'y']:
    cache_conn = cache.init_cache()
    cache_conn.flushall(cache_conn)
    print("All data in the Redis cache has been deleted.")
else:
    print("Data deletion aborted.")
