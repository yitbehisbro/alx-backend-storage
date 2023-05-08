#!/usr/bin/env python3
""" Top students """


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    orders = [
        {"$unwind": "$scores"},
        {"$group": {"_id": "$_id", "averageScore": {"$avg": "$scores.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(orders))
