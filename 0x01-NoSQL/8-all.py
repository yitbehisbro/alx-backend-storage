#!/usr/bin/env python3
""" Lists all the documents """


def list_all(mongo_collection):
    """List all documents in collection using Python function
    """
    return list(mongo_collection.find())
