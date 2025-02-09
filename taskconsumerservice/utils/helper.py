
import uuid
from datetime import datetime


def generate_default_pk():
    return str(uuid.uuid4()).replace("-", "")


def get_current_unix_timestamp_ms() -> int:
    """Returns the current Unix timestamp in milliseconds."""
    return int(datetime.now().timestamp() * 1000)

def convert_datetime_to_unix_ms(dt: datetime) -> int:
    """Converts a datetime object to Unix timestamp in milliseconds."""
    return int(dt.timestamp() * 1000)

def convert_unix_ms_to_datetime(unix_ms: int) -> datetime:
    """Converts a Unix timestamp in milliseconds to a datetime object."""
    return datetime.fromtimestamp(unix_ms / 1000)

