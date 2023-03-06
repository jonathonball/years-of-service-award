import redis
import argparse

r = redis.Redis(host='localhost', port=6379, db=0)

parser = argparse.ArgumentParser()
parser.add_argument('--force', '-f', action='store_true', help='skip confirmation prompt')
args = parser.parse_args()

if not args.force:
  confirmation = input("Are you sure you want to delete all data in the Redis cache? (Yes/No)")

if args.force or confirmation.lower() in ['yes', 'y']:
    r.flushall()
    print("All data in the Redis cache has been deleted.")
else:
    print("Data deletion aborted.")
