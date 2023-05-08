#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_logs = {}
    for m in methods:
        method_logs[m] = collection.count_documents({"method": m})

    status_l = collection.count_documents({"method": "GET", "path": "/status"})

    print("{} logs".format(total_logs))
    print("Methods:")
    for method, count in method_logs.items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(status_l))
