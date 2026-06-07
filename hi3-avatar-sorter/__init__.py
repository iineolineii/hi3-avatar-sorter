import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__package__)

__vesrion__ = (0, 0, 2)

__all__ = ["log", "__vesrion__"]
