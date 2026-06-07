import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__package__)

__vesrion__ = (0, 0, 1)

__all__ = ["log", "__vesrion__"]
