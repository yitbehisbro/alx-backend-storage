#!/usr/bin/env python3
""" Updates all the school documents """


def update_topics(mongo_collection, name, topics):
    """ Updates the school collection """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
