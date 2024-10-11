import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CheckEnvironment:

    def __init__(self):
        pass

    @staticmethod
    def get_env(keys: list) -> dict:
        rc = {}

        for key in keys:
            if key not in os.environ or not os.environ[key]:
                rc[key] = None
            else:
                rc[key] = os.environ[key]

        return rc

    @staticmethod
    def check_keys(keys: list, args: dict) -> bool:
        rc = True

        for key in keys:
            if key not in args or not args[key]:
                logger.error(f"The variable {key} is missing or has a null value.")
                rc = rc and False

        return rc
