import time
import logging
from typing import Callable, TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)


def retry(
        func: Callable[..., T],
        retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        *args,
        **kwargs
) -> T:
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == retries - 1:
                raise
            sleep_time = delay * (backoff ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {sleep_time:.2f}s")
            time.sleep(sleep_time)
