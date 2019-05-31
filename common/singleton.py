"""Singleton decorator."""


def singleton(cls, *arg, **kw):
    """A singleton decorator."""
    instances = {}

    def _singleton(*arg, **kw):
        if cls not in instances:
            instances[cls] = cls(*arg, **kw)
        return instances[cls]
    return _singleton
