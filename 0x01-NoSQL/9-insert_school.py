#!/usr/bin/env python3
""" Inserts data """


def insert_school(mongo_collection, **kwargs):
    """ Returns Id of new inserts """
    return mongo_collection.insert_one(kwargs).inserted_id
