class DBConnectionError(Exception):
    """When could not connect to database"""


class ElementNotFoundError(Exception):
    """When element not found in DB"""


class InsertionError(Exception):
    """When there was a problem while inserting a DB"""
